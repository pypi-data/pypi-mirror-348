from async_timeout import asyncio
from diskcache import Cache
from threading import Lock
from urllib.parse import urlparse

from hamunafs.backends.fetcher import file_fetcher
from hamunafs.utils.singleton_wrapper import Singleton
from hamunafs.utils.redisutil import XRedis
from hamunafs.utils.nsqmanager import MQManager
from hamunafs.utils.minio_async import MinioAsync
from hamunafs.backends import BackendBase, backend_factory

import uuid
import random
import os
import shutil
import time
import threading
import json
import httpx
import traceback
import telnetlib
try:
    import nest_asyncio
    nest_asyncio.apply()
except:
    pass

class Client(Singleton):
    def __init__(self, host, redis_client, cache_path='../cache', workers=8, put_topic='fs_put', get_topic='fs_get', health_topic='fs_health') -> None:
        if not self.need_init():
            return
        
        self.host = host
        self.redis = redis_client
        
        self.lock = Lock()
        
        #self.cache_path = cache_path
        if cache_path is not None:
            os.makedirs(cache_path, exist_ok=True)
        self.index_cache = Cache(cache_path)
        
        self.put_topic = put_topic
        self.get_topic = get_topic
        self.health_topic = health_topic

        self.backend_pools = {}
        self.direct_nodes_clients = {}
        
        self.update()
        self._inited = True

        self.backend_updating = False

        self.sem = asyncio.Semaphore(workers)

        self.background_updater = threading.Thread(target=self.update_loop, daemon=True)
        self.background_updater.start()

    def get_qiniu_token(self, fname):
        qiniu_backend_keys = [k for k in list(self.backend_pools.keys()) if k.startswith('qiniu')]
        if len(qiniu_backend_keys) > 0:
            backend_key = random.sample(qiniu_backend_keys, 1)[0]
            backend = self.backend_pools[backend_key]
            return backend.get_token(fname)
        return None

    def decode_download_url(self, encode_url):
        backend, bucket, bucket_name = self._get_appropriate_backend(encode_url)
        return backend.geturl('{}/{}'.format(bucket, bucket_name))
    
    def update_loop(self):
        while True:
            try:
                print('running background updater...')
                if time.time() - self.last_update_time > 60 * 5:
                    self.update(force=True)
                    time.sleep(60)
                else:
                    print('waiting for next update...')
                    time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(5)

    def update(self, force=False):
        if self._inited and not force:
            return
        self.update_backends(force=force)
        self.update_nodes()
        
        self.last_update_time  = time.time()
    
    def update_backends(self, force=False):
        print('updating backends...')
        if self.host.startswith('http'):
            api_path = '{}/api/system/fs/backends'.format(self.host)
        else:
            api_path = 'https://{}/api/system/fs/backends'.format(self.host)
        resp = httpx.get(api_path, headers={
            'from': 'edge'
        }, timeout=httpx.Timeout(60), verify=False)
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            if resp['success'] == 'ok':
                print('backend cfg loaded')
                backend_pools = {}
                fallback_pools = {}
                pool_data = resp['data']
                for info in pool_data:
                    if info['type'] == 'temp':
                        backend_pools[info['key']] = backend_factory[info['backend']](info['conf'])
                    else:
                        fallback_pools[info['key']] = backend_factory[info['backend']](info['conf'])
                
                self.backend_updating = True
                self.backend_pools = backend_pools
                self.fallback_pools = fallback_pools
                self.backend_updating = False

            else:
                raise Exception('error on acquiring fs backends...')
        else:
            raise Exception('error on acquiring fs backends...')
        
    def _build_direct_clients(self):
        for node in self.nodes:
            if node['connected'] and node['id'] not in self.direct_nodes_clients:
                # check endpoint accessable
                if 'minio_endpoint' in node['status']:
                    host, port = node['status']['minio_endpoint']['endpoint'].split(':')
                    try:
                        telnetlib.Telnet(node['tun_ip'], int(port), timeout=2)
                        node['status']['minio_endpoint']['endpoint'] = '{}:{}'.format(node['tun_ip'], port)
                        self.direct_nodes_clients[node['id']] = MinioAsync(**node['status']['minio_endpoint'])
                    except Exception as e:
                        print(e)
            elif not node['connected'] and node['id'] in self.direct_nodes_clients:
                del self.direct_nodes_clients[node['id']]

    def update_nodes(self):
        print('updating nodes...')
        if self.host.startswith('http'):
            api_path = '{}/api/system/fs/nodes'.format(self.host)
        else:
            api_path = 'https://{}/api/system/fs/nodes'.format(self.host)
        resp = httpx.get(api_path, headers={
            'from': 'edge'
        }, timeout=httpx.Timeout(60), verify=False)
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            if resp['success'] == 'ok':
                nodes = resp['data']

                self.node_updating = True
                self.nodes = nodes
                self.root_node_id = [n['id'] for n in nodes if n['root']][0]
                self._build_direct_clients()
                self.node_updating = False
            else:
                raise Exception('error on acquiring fs backends...')
        else:
            raise Exception('error on acquiring fs backends...')
                

    def _wait_lock(self, timeout=10):
        t = time.time()
        while self.backend_updating:
            time.sleep(1)
            if time.time() - t > timeout:
                return False
        
        return True
    
    def _node_wait_lock(self, timeout=5):
        t = time.time()
        while self.node_updating:
            time.sleep(1)
            if time.time() - t > timeout:
                return False
        
        return True

    def _check_backends(self):
        return len([n for n in self.nodes if n['status']['minio'] and n['connected'] and n['status']['disk']['free'] > 1]) > 0
    
    def _random_pick_node(self):
        if self._node_wait_lock():
            matched_nodes = [n for n in self.nodes if n['status']['minio'] and n['connected'] and n['status']['disk']['free'] > 1]

            if len(matched_nodes) > 1:
                selected_ind = int(random.uniform(0, len(matched_nodes)))
                selected_node = matched_nodes[selected_ind]
            else:
                selected_node = matched_nodes[0]


            return selected_node
        return None
        
    def _random_pick_backend(self, ignore_prefix=[], fallback=False) -> BackendBase:
        pools = self.backend_pools if not fallback else self.fallback_pools
        if self._wait_lock():
            keys = [k for k in list(pools.keys()) if k not in ignore_prefix]
            if len(keys) > 0:
                selected_ind = random.choices(range(len(keys)))[0]
                
                selected_key = keys[selected_ind]
                print('choosing {} backend'.format(selected_key))
                return selected_key, pools[selected_key]
            
        return None, None
    
    def _get_appropriate_backend(self, url):
        if self._wait_lock():
            prefix, _url = url.split('://')
            pools = self.backend_pools if 'fallback-' not in prefix else self.fallback_pools

            prefix = prefix.replace('fallback-', '')
            
            if prefix in pools:
                if '/' in _url:
                    bucket, bucket_name = _url.split('/')
                elif '_' in _url:
                    bucket, bucket_name = _url.split('_')
                else:
                    return None, None, None
                return pools[prefix], bucket, bucket_name
        return None, None, None

    def _get_backend(self, key):
        return key, self.backend_pools[key]

    async def get_cache_async(self, key, toObj=True):
        data = self.index_cache.get(key)
        if data is None:
            if self.redis is not None:
                data = await self.redis.get(key)

        if data is not None and toObj:
            data = json.loads(data)
        
        return data

    async def cache_async(self, key, val, ttl=7200):
        if not isinstance(val, str):
            _val = json.dumps(val)
        else:
            _val = val
        try:
            await self.redis.set(key, _val, expired=ttl)
        except:
            pass
        self.index_cache.set(key, _val, expire=ttl)

    async def __put_to_cloud_async(self, path, bucket, bucket_name, tmp=True, tries=0, ignore_prefix=[]):
        prefix, backend = self._random_pick_backend(ignore_prefix)
        if prefix is None:
            return False, '尝试过所有Backend都失败'
        
        ret, e = await backend.put_async(path, bucket, bucket_name, tmp)
        if ret:
            url = '{}://{}'.format(prefix, e)
            return True, url
        else:
            ignore_prefix.append(prefix)
            return await self.__put_to_cloud_async(path, bucket, bucket_name, tmp, tries+1, ignore_prefix=ignore_prefix)

    async def put_to_cloud_async(self, path, bucket, bucket_name, tmp=True, refresh=False):
        cache_key = 'cloud_{}_{}'.format(bucket, bucket_name)
        cache_data = await self.get_cache_async(cache_key, toObj=False) if not refresh else None
        if cache_data is None:
            if os.path.isfile(path):
                ret, e = await self.__put_to_cloud_async(path, bucket, bucket_name, tmp, tries=0, ignore_prefix=[])
                if ret:
                    await self.cache_async(cache_key, e, 3600 * 24)
                return ret, e
            else:
                return False, '文件不存在'
        else:
            return True, cache_data
    
    async def get_from_cloud_async(self, path, url, force_copy=False, min_size=0, refresh=False):
        file_path = self.index_cache.get(url)
        if file_path is not None and os.path.isfile(file_path) and os.path.getsize(file_path) // 1024 >= min_size and not refresh:
            print('loading from disk...')
            if force_copy:
                # prefix = url.split('://')[0].replace('fallback-', '')
                if file_path == path:
                    return True, path
                else:
                    os.makedirs(os.path.split(path)[0], exist_ok=True)
                    
                    shutil.copy(file_path, path)
                    
                    return True, path
            return True, file_path             
        
        
        backend, bucket, bucket_name = self._get_appropriate_backend(url)

        print('loading from redis...')
        cache_key = 'cloud_{}_{}'.format(bucket, bucket_name)
        cache_data = await self.get_cache_async(cache_key, toObj=False) if not refresh else None
        if cache_data:
            try:
                path = await file_fetcher.fetch_file_async(cache_data, path)
                self.index_cache.set(url, path)

                return True, path
            except Exception as e:
                traceback.print_exc()
        
        print('loading from cloud...')
        if backend is not None:
            ret, e = await backend.get_async(path, bucket, bucket_name)
            if ret:
                self.index_cache.set(url, e)
                return True, path
            else:
                return ret, e
        else:
            return False, '未受支持的Backend'

    async def direct_get(self, node_id, path, bucket, bucket_name):
        client: MinioAsync = self.direct_nodes_clients.get(node_id, None)
        if client:
            return await client.download_file(path, bucket, bucket_name)
        else:
            return False, None

    async def get_async(self, path, url, force_copy=False, min_size=0, timeout=60, refresh=False):
        async with self.sem:
            if 'fallback-' in url:
                return await self.get_from_cloud_async(path, url, force_copy, min_size, refresh)
            elif '://' in url:
                object_url = url.split('://')[1]
                node_id = self.root_node_id
                bucket, bucket_name = object_url.split('/')
            else:
                if ':' in url:
                    node_id = url.split(':')[0]
                    _path = url.split(':')[1]
                    bucket, bucket_name = _path.split('/')
                else:
                    node_id = self.root_node_id
                    bucket, bucket_name = url.split('/')
            task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
            if not refresh:
                if '://' in url:
                    ret, e = await self.get_from_cloud_async(path, url, force_copy, min_size)
                    return ret, e
                
                print('downloading {}...'.format(url))

                cached_resp = await self.redis.get(task_id)

                if cached_resp is not None and len(cached_resp) > 0:
                    resp = json.loads(cached_resp)
                    if resp['ret']:
                        tmp_url = resp['url']
                        return await self.get_from_cloud_async(path, tmp_url, force_copy, min_size)
            else:
                await self.redis.delkey(task_id)

            try:
                node_info = [n for n in self.nodes if n['id'] == node_id]
                if len(node_info) > 0:
                    node_info = node_info[0]
                if node_info['connected'] and node_info['status']['minio']:
                    ret, e = await self.direct_get(node_id, path, bucket, bucket_name)
                    if not ret:
                        ret = await self.async_publish('{}_{}'.format(self.get_topic, node_id), {
                            'bucket': bucket,
                            'bucket_name': bucket_name,
                            'refresh': 'yes' if refresh else 'no'
                        })
                        if ret:
                            t = time.time()
                            resp = None
                            while True:
                                if time.time() - t >= timeout:
                                    break
                                
                                resp = await self.redis.get(task_id)
                                if resp is not None and len(resp) > 0:
                                    resp = json.loads(resp)
                                    if resp['ret']:
                                        tmp_url = resp['url']
                                        return await self.get_from_cloud_async(path, tmp_url, force_copy, min_size, refresh=True)
                                    else:
                                        return False, resp['err']
                                
                                await asyncio.sleep(1/30)
                            return False, '超时'
                        else:
                            return False, 'MQ发送失败'
                    else:
                        print('direct get success -> {}'.format(url))
                        return ret, e
                else:
                    return False, '节点错误'
            except Exception as e:
                return False, '获取失败'
    
    async def get_cloud_url_async(self, path, url, force_copy=False, min_size=0, timeout=60, refresh=False):
        if '://' in url:
            bucket, bucket_name = url.split('://')[1].split('/')
        else:
            bucket, bucket_name = url.split('/')
            
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        if not refresh:
            if '://' in url:
                return True, url

            cached_resp = await self.redis.get(task_id)

            if cached_resp is not None and len(cached_resp) > 0:
                resp = json.loads(cached_resp)
                if resp['ret']:
                    tmp_url = resp['url']
                    return True, tmp_url
        else:
            await self.redis.delkey(task_id)
        
        try:
            ret = await self.async_publish(self.get_topic, {
                'bucket': bucket,
                'bucket_name': bucket_name,
                'refresh': 'yes' if refresh else 'no'
            })
            if ret:
                t = time.time()
                resp = None
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = await self.redis.get(task_id)
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            tmp_url = resp['url']
                            return True, tmp_url
                    
                    await asyncio.sleep(1/30)
        except Exception as e:
            return False, '获取失败'
    
    async def async_publish(self, topic, message, tries=0):
        if tries > 3:
            return False
        async with httpx.AsyncClient(timeout=20) as client:
            try:
                if self.host.startswith('http'):
                    api_path = '{}/api/trade/platform/common_api/nsq_pub'.format(self.host)
                else:
                    api_path = 'https://{}/api/trade/platform/common_api/nsq_pub'.format(self.host)
                r = await client.post(api_path, json={
                    'topic': topic,
                    'message': message
                }, headers={
                    'from': 'edge'
                })
                if r.status_code == 200:
                    r = json.loads(r.text)
                    if r['success'] == 'ok':
                        return True
                    else:
                        return False
            except Exception as e:
                traceback.print_exc()
                print('发布出错, 等待重试')
                await asyncio.sleep(0.5)
                return await self.async_publish(topic, message, tries+1)

    async def put_from_cloud_async(self, url, bucket, bucket_name, timeout=120, tries=0, file_ttl=-1):
        # save to cache
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        try:
            ret = await self.async_publish(self.put_topic, {
                'url': url,
                'bucket': bucket,
                'bucket_name': bucket_name,
                'ttl': file_ttl
            })
            if ret:
                t = time.time()
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = await self.redis.get(task_id)
                    
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            return True, '{}:{}/{}'.format(resp['node'], bucket, bucket_name)
                        else:
                            return False, '{}: {}'.format(resp['node'], resp['err'])
                    
                    await asyncio.sleep(1/30)
                if tries < 3:
                    return await self.put_from_cloud_async(url, bucket, bucket_name, timeout, tries+1, file_ttl)
                else:
                    return False, '等待文件服务回执超时， 可能是文件服务器发生错误'
            else:
                if tries < 3:
                    return await self.put_from_cloud_async(url, bucket, bucket_name, timeout, tries+1, file_ttl)
                else:
                    return False, '推送到MQ失败'
        except Exception as e:
            return False, str(e)
    
    async def put_async(self, path, bucket, bucket_name, timeout=60, file_ttl=-1):
        async with self.sem:
            ret = self._check_backends()
            if ret:
                ret, e = await self.put_to_cloud_async(path, bucket, bucket_name)
                if ret:
                    ret, e = await self.put_from_cloud_async(e, bucket, bucket_name, timeout, file_ttl)
            else:
                ret, e = await self.try_fallback(path, bucket, bucket_name)
            return ret, e
        
    
    async def try_fallback(self, path, bucket, bucket_name, ignore_prefix=[]):
        if len(self.fallback_pools) > 0:
            backend_key, backend = self._random_pick_backend( ignore_prefix=ignore_prefix, fallback=True)

            if backend_key:
                if os.path.isfile(path):
                    ret, e = await backend.put_async(path, bucket, bucket_name, False)
                    if ret:
                        url = 'fallback-{}://{}'.format(backend_key, e)
                        return True, url
                    else:
                        ignore_prefix.append(backend_key)
                        return await self.try_fallback(path, bucket, bucket_name, ignore_prefix)
                else:
                    return False, '文件不存在'
        return False, '没有可用的fallback'
    
    def geturl(self, entrypoint):
        prefix, bucket_info = entrypoint.split('://')
        if prefix in self.backend_pools:
            backend = self.backend_pools[prefix]
            return backend.geturl(bucket_info)
        else:
            return entrypoint

    async def cleanup_cloud(self):
        for k, backend in self.backend_pools.items():
            print('cleanup {} files'.format(k))
            await backend.cleanup_old_files()
    
    async def health_check(self, timeout=10):
        task_id = str(uuid.uuid1())
        ret = await self.async_publish(self.health_topic, {
            'task_id': task_id
        })

        if ret:
            t = time.time()
            while True:
                if time.time() - t >= timeout:
                    break
                
                resp = await self.redis.get('fs_health_{}'.format(task_id))
                if resp is not None and len(resp) > 0:
                    resp = json.loads(resp)
                    if resp['ret']:
                        return True, resp['status']
                    else:
                        return False, resp['err']
                
                await asyncio.sleep(1/30)
            return False, '等待回执超时'
        else:
            return False, '推送到MQ失败'