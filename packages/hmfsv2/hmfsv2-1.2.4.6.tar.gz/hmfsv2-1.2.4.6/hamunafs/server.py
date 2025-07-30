import traceback
# from function_scheduling_distributed_framework import fsdf_background_scheduler, task_deco, patch_frame_config, get_publisher, BrokerEnum
# from function_scheduling_distributed_framework.consumers.base_consumer import ExceptionForRequeue

from funboost import boost as task_deco, fsdf_background_scheduler, get_publisher, BrokerEnum, ConcurrentModeEnum, BoosterParams
from funboost.consumers.base_consumer import ExceptionForRequeue

from hamunafs.utils.cachemanager import CacheManagerAsync, Cache
from hamunafs.utils.minio_async import MinioAgentAsync
from hamunafs.v2.client import Client as FSClient

import netifaces
import uvloop
import asyncio
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# import nest_asyncio
# nest_asyncio.apply()

import time
import os
import argparse
import shutil
import json
import httpx
import copy
import netifaces
from hamunafs.sqlite import DB
from hamunafs.utils.timeutil import is_time_in_range


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', type=str, default='brick1')
    # parser.add_argument('--root-path', type=str, default='/media/hdd0/platform/hamunafs/hmfs_data')
    # parser.add_argument('--cfg-path', type=str, default='/media/hdd0/platform/hamunafs/hmfs_conf')
    parser.add_argument('--root-path', type=str, default='../hmfs_data')
    parser.add_argument('--cfg-path', type=str, default='../hmfs_conf')
    parser.add_argument('--api-host', type=str,
                        default='backend.ai.hamuna.club')
    parser.add_argument('--redis-host', type=str,
                        default='cache.ai.hamuna.club')
    parser.add_argument('--redis-port', type=int, default=6379)
    parser.add_argument('--redis-pass', type=str, default='1987yang')
    parser.add_argument('--redis-db', type=int, default=2)

    opt = parser.parse_args()
    return opt


opt = get_opts()

root_path = opt.root_path

cache_path = os.path.join(root_path, 'cache')
db_path = os.path.join(root_path, 'db')

os.makedirs(cache_path, exist_ok=True)
os.makedirs(db_path, exist_ok=True)

# init sqlite
sqlite_db = DB(os.path.join(db_path, 'data.sqlite3'), is_relative=False)

sqlite_db.create_table('ttl_files', [
                       "id integer PRIMARY KEY", "bucket text NOT NULL", "bucket_name text NOT NULL", "expired integer"])

last_in_msg_ts = time.time()
last_ping = time.time()
local_queue_get = time.time()
local_queue_put = time.time()

local_queue_timeout = 0

def check_cfg(cfg):
    if len(cfg['NODE_ID']) == 24 and len(cfg['FS_HOST']) > 0 and len(cfg['FS_HOST']) == len(cfg['HOST_WEIGHTS']):
        return True
    return False

if os.path.isfile(os.path.join(opt.cfg_path, 'hmfs.cfg')):
    cfg = json.load(open(os.path.join(opt.cfg_path, 'hmfs.cfg'), 'r'))
    if check_cfg(cfg):
        pass
    else:
        print('配置文件不合法')
        exit(-1)
else:
    os.makedirs(opt.cfg_path, exist_ok=True)
    template = {
        "NODE_ID": "",
        "FS_HOST": ["127.0.0.1:9000"],
        "HOST_WEIGHTS": [5],
        "HOST_AUTH": [
            {
                "acs_key": "",
                "acs_secret": ""
            }
        ]
    }
    json.dump(template, open(os.path.join(opt.cfg_path, 'hmfs.cfg'), 'w'))
    print('已生成配置文件，请修改配置文件后重新启动')
    exit(-1)

endpoints = [{
    'endpoint': host, 
    'access_key': auth['acs_key'],#opt.acs_key, 
    'secret_key': auth['acs_secret'],#opt.acs_secret, 
    'secure': False,
    'region': auth.get('location', None)
} for host, auth in zip(cfg['FS_HOST'], cfg['HOST_AUTH'])]

exception_queue = []
last_exception_sync_time = 0

minio = MinioAgentAsync(endpoints, list(map(int, cfg['HOST_WEIGHTS'])), check_awailable_ts=10, timeout=30)

cache_engine_async = CacheManagerAsync(
    opt.redis_host, opt.redis_pass, opt.redis_port, opt.redis_db, local_cache=None)

local_cache = Cache(cache_path)

# patch_frame_config(
#     NSQD_TCP_ADDRESSES=['{}:{}'.format(opt.broker_host, opt.broker_port)],
#     NSQD_HTTP_CLIENT_HOST=opt.broker_host,
#     NSQD_HTTP_CLIENT_PORT=opt.broker_http_port,
# )

hmfs_client = FSClient(opt.api_host, cache_engine_async.client, None)
consumer_loop = asyncio.new_event_loop()
local_loop = asyncio.new_event_loop()

def append_exception(exception, url, bucket, bucket_name):
    exception_queue.append({
        'exception': exception,
        'url': url,
        'bucket': bucket,
        'bucket_name': bucket_name,
        'timetag': time.time()
    })

def sync_exceptions(exceptions):
    if len(exceptions) > 0:
        print('sync exceptions...')
        resp = httpx.post('https://{}/api/system/fs/add_exception_logs'.format(opt.api_host), json={
            'node_id': cfg['NODE_ID'],
            'exceptions': exceptions
        })
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            if resp['success'] == 'ok':
                print('sync success')
                return True
        return False
    
#specify_async_loop=asyncio.get_event_loop()
@task_deco('fs_put', function_timeout=120, concurrent_mode=ConcurrentModeEnum.ASYNC, concurrent_num=10, broker_kind=BrokerEnum.NSQ, specify_async_loop=consumer_loop, max_retry_times=1)
async def file_transfer_put(url, bucket, bucket_name, ttl):
    global last_in_msg_ts, local_queue_timeout
    # ret = await file_transfer_put_local(url, bucket, bucket_name, ttl)
    file_transfer_put_local.push(url, bucket, bucket_name, ttl, False)
    last_in_msg_ts = time.time()
    # local_cache.set('fs_put_{}'.format(url), 0, expire=40)
    # await asyncio.sleep(1)
    # resp = local_cache.get('fs_put_{}'.format(url))
    # while resp != 1:
    #     if resp is None:
    #         local_queue_timeout += 1
    #         return False
    #     else:
    #         await asyncio.sleep(0.1)
    #         resp = local_cache.get('fs_put_{}'.format(url))
    
    # local_queue_timeout = 0

    return True

@task_deco('fs_put_local', function_timeout=120, concurrent_mode=ConcurrentModeEnum.ASYNC, broker_kind=BrokerEnum.LOCAL_PYTHON_QUEUE, max_retry_times=1)
async def file_transfer_put_local(url, bucket, bucket_name, ttl, test=False):
    global local_queue_put
    local_queue_put = time.time()
    if test:
        print('响应 put queue test')
        return True
    try:
        key = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        cached_resp = await cache_engine_async.get_cache(key, return_obj=True)
        if cached_resp is not None and cached_resp['ret']:
            return True
        file_path = os.path.join(
            cache_path, '{}_{}'.format(bucket, bucket_name))
        ret, file_path = await hmfs_client.get_from_cloud_async(file_path, url)

        if ret:
            print('cloud downloaded. start uploading...')
            ret, e = await minio.upload_file(file_path, bucket, bucket_name)
            if ret:
                print('uploaded. writing to redis middleware...')
                await cache_engine_async.cache(key, {
                    'ret': True,
                    'node': cfg['NODE_ID'],
                    'url': url,
                    'ts': time.time()
                }, expired=24 * 60 * 60)
                print('upload success!!')
                try:
                    os.remove(file_path)
                    print('remove file success')
                except Exception as e:
                    print(e)

                if ttl != -1:
                    expired_time = time.time() + ttl * 24 * 60 * 60
                    sqlite_db.iud('insert into ttl_files(bucket, bucket_name, expired) values (?, ?, ?)', (
                        bucket, bucket_name, expired_time))
                return True
            else:
                print('upload failed. writing to redis middleware...')
                await cache_engine_async.cache('tmp_file_{}_{}'.format(bucket, bucket_name), {
                    'ret': False,
                    'node': cfg['NODE_ID'],
                    'err': e,
                    'ts': time.time()
                }, expired=5)
                return False
        else:
            print('fput -> cloud download failed')
            await cache_engine_async.cache('tmp_file_{}_{}'.format(bucket, bucket_name), {
                'ret': False,
                'node': cfg['NODE_ID'],
                'err': '文件中转错误',
                'ts': time.time()
            }, expired=5)
            return False
    except Exception as e:
        exception = traceback.format_exc()
        append_exception(exception, url, bucket, bucket_name)
        print(exception)
        await cache_engine_async.cache('tmp_file_{}_{}'.format(bucket, bucket_name), {
            'ret': False,
            'node': cfg['NODE_ID'],
            'err': exception,
            'ts': time.time()
        }, expired=5)
        return False

async def put_to_cloud(task_id, file_path, bucket, bucket_name, refresh=False, tries=0):
    ret, e = await hmfs_client.put_to_cloud_async(
        file_path, bucket, bucket_name, refresh=refresh)
    if ret:
        print('fget -> uploaded to cloud')
        await cache_engine_async.cache(task_id, {
            'ret': True,
            'node': cfg['NODE_ID'],
            'url': e,
            'time': time.time()
        }, expired=5 * 60 * 24 * 1)
        ext = os.path.splitext(file_path)[-1]
        if ext not in ['.jpg', '.jpeg', '.png']:
            try:
                os.remove(file_path)
                print('remove file success')
            except Exception as e:
                print(e)
    else:
        if tries > 3:
            print('fget -> failed uploading to cloud')
            await cache_engine_async.cache(task_id, {
                'ret': False,
                'node': cfg['NODE_ID'],
                'err': e,
                'time': time.time()
            }, expired=5)
        else:
            print('fget -> retry put to cloud')
            await put_to_cloud(task_id, file_path, bucket, bucket_name,
                         refresh=refresh, tries=tries+1)

@task_deco('fs_get_{}'.format(cfg['NODE_ID']), function_timeout=60, concurrent_mode=ConcurrentModeEnum.ASYNC, concurrent_num=10, broker_kind=BrokerEnum.NSQ, specify_async_loop=consumer_loop, max_retry_times=1)
async def file_transfer_get(bucket, bucket_name, refresh='no'):
    global last_in_msg_ts, local_queue_timeout
    last_in_msg_ts = time.time()
    file_transfer_get_local.push(bucket, bucket_name, refresh, False)
    
    # key = 'fs_get_{}_{}'.format(bucket, bucket_name)
    # print('设置相应标签: {}'.format(key))
    # local_cache.set('fs_get_{}_{}'.format(bucket, bucket_name), 0, expire=40)
    # await asyncio.sleep(1)
    # resp = local_cache.get('fs_get_{}_{}'.format(bucket, bucket_name))
    
    # while resp != 1:
    #     if resp is None:
    #         print('本地队列超时 -> {}'.format(key))
    #         local_queue_timeout += 1
    #         return False
    #     else:
    #         await asyncio.sleep(0.1)
    #         resp = local_cache.get('fs_get_{}_{}'.format(bucket, bucket_name))
    
    # print('本地队列响应正常 -> {}'.format(key))
    # local_queue_timeout = 0

    return True

@task_deco('fs_get_{}_local'.format(cfg['NODE_ID']), function_timeout=60, concurrent_mode=ConcurrentModeEnum.ASYNC, broker_kind=BrokerEnum.LOCAL_PYTHON_QUEUE, max_retry_times=2)
async def file_transfer_get_local(bucket, bucket_name, refresh='no', test=False):
    global local_queue_get

    local_queue_get = time.time()
    if test:
        print('响应 get queue test')
        return True
    try:
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        file_path = os.path.join(
            cache_path, '{}_{}'.format(bucket, bucket_name))
        if not os.path.isfile(file_path) or refresh == 'yes':
            try:
                print('fget -> downloading {} from {} {}'.format(file_path, bucket, bucket_name))
                ret, e = await minio.download_file(file_path, bucket, bucket_name)
                if ret:
                    print('fget -> downloaded from minio')
                    file_path = e
                else:
                    print('fget -> failed from minio')
                    await cache_engine_async.cache(task_id, {
                        'ret': False,
                        'node': cfg['NODE_ID'],
                        'err': '获取错误 -> {}'.format(e),
                        'ts': time.time()
                    }, expired=5)
                    return False
            except Exception as e:
                await cache_engine_async.cache(task_id, {
                        'ret': False,
                        'node': cfg['NODE_ID'],
                        'err': str(e),
                        'time': time.time()
                    }, expired=5)
                return False

        await put_to_cloud(task_id, file_path, bucket,
                     bucket_name, refresh=refresh == 'yes')
        return True
    except Exception as e:
        traceback.print_exc()
        await cache_engine_async.cache(task_id, {
            'ret': False,
            'node': cfg['NODE_ID'],
            'err': str(e),
            'time': time.time()
        }, expired=5)
        return False

import psutil
def low_disk():
    disk = psutil.disk_usage(opt.root_path)
    # Convert Bytes to GB (Bytes -> KB -> MB -> GB)
    disk_free = round(disk.free/1024.0/1024.0/1024.0,1)
    return disk_free < 3

def get_system_status():
    global opt, last_ping
    # Get cpu statistics
    cpu = str(psutil.cpu_percent())

    # Calculate memory information
    memory = psutil.virtual_memory()
    # Convert Bytes to MB (Bytes -> KB -> MB)
    mem_available = round(memory.available/1024.0/1024.0,1)
    mem_total = round(memory.total/1024.0/1024.0,1)
    

    # Calculate disk information
    disk = psutil.disk_usage(opt.root_path)
    # Convert Bytes to GB (Bytes -> KB -> MB -> GB)
    disk_free = round(disk.free/1024.0/1024.0/1024.0,1)
    disk_total = round(disk.total/1024.0/1024.0/1024.0,1)


    minio_status = minio.availability[0]
    minio_endpoint = minio.endpoints[0]
    long_idle_warning = time.time() - last_in_msg_ts > 60

    return {
        'cpu': cpu,
        'memory': {
            'free': mem_available,
            'total': mem_total
        },
        'disk': {
            'free': disk_free,
            'total': disk_total
        },
        'minio': minio_status,
        'minio_endpoint': minio_endpoint,
        'long_idle': long_idle_warning
    }

from hamunafs.net.api import send

def get_tun_ip():
    interfaces = netifaces.interfaces()
    if 'vnt-tun' in interfaces:
        return netifaces.ifaddresses('vnt-tun')[netifaces.AF_INET][0]['addr']
    return 'na'

async def ping_host():
    post_params = {
        'node_id': cfg['NODE_ID'],
        'node_status': get_system_status(),
        'node_tun_ip': get_tun_ip()
    }
    print(post_params)
    resp = await send('https://{}/api/system/fs/node_ping'.format(opt.api_host), 'post', post_params, headers={
        'from': 'edge'
    }, timeout=3)
    if resp and resp['success'] == 'ok':
        return True
    return False
    
async def ttl_cleanup():
    rows = sqlite_db.select(
        'select id, bucket, bucket_name from ttl_files where expired < ?', (time.time(),))
    affected_records = 0
    if rows is not None:
        for r in rows:
            bucket, bucket_name = r['bucket'], r['bucket_name']
            ret, e = await minio.delete(bucket, bucket_name, 0)
            if ret:
                affected_records += 1
                print('removing file id: {} from db...'.format(r['id']))
                sqlite_db.iud(
                    'delete from ttl_files where id={};'.format(r['id']))
            else:
                print(e)

    return affected_records

@task_deco('fs_ping_{}'.format(cfg['NODE_ID']), function_timeout=60, concurrent_mode=ConcurrentModeEnum.ASYNC, concurrent_num=1, broker_kind=BrokerEnum.NSQ, max_retry_times=1)
async def fs_ping():
    global last_in_msg_ts
    last_in_msg_ts = time.time()

    try:
        ret = await ping_host()
        if ret:
            print('node ping success')
        else:
            print('node ping failed')
    except Exception as e:
        return False
    return True

async def extra_tasks():
    global exception_queue, last_exception_sync_time, last_in_msg_ts, local_queue_timeout, local_queue_put, local_queue_get
    while True:
        try:
            affected_records = await ttl_cleanup()
            if affected_records > 0:
                print('data cleaned')

            print('测试 local get queue')
            file_transfer_get_local.push('', '', 'no', True)
            print('测试 local put queue')
            file_transfer_put_local.push('', '', '', 0, True)

            # if len(exception_queue) > 5 or time.time() - last_exception_sync_time > 60:
            #     will_post_exceptions = copy.deepcopy(exception_queue)
            #     ret = sync_exceptions(will_post_exceptions)
            #     if ret:
            #         for exception in will_post_exceptions:
            #             exception_queue.remove(exception)
            #         last_exception_sync_time = time.time()
            #     else:
            #         print(will_post_exceptions)

            if time.time() - local_queue_put > 300:
                print('本地队列超时, 退出程序')
                os._exit(0)

            if time.time() - local_queue_get > 300:
                print('本地队列超时, 退出程序')
                os._exit(0)

            if time.time() - last_in_msg_ts > 300:
                print('长时间未能检测到入队消息，退出程序')
                os._exit(0)

            if low_disk():
                print('磁盘空间不足， 暂停上传接口，重启程序')
                os._exit(0)

            ret = await ping_host()
            if ret:
                print('node ping success')
            else:
                print('node ping failed')
                
            if is_time_in_range('02:00', '04:00'):
                if await cache_engine_async.get_cache('hmfs_cleanup'):
                    continue
                await hmfs_client.cleanup_cloud()
                await cache_engine_async.cache('hmfs_cleanup', 1, expired=7200)
                # shutil.rmtree(cache_path, ignore_errors=True)
                # os.mkdir(cache_path)
            
        except:
            traceback.print_exc()
        finally:
            await asyncio.sleep(30)


def run():
    file_transfer_get.consume()
    file_transfer_get_local.consume()
    if not low_disk():
        print('starting put transfer...')
        file_transfer_put.consume()
        file_transfer_put_local.consume()
    # fs_ping.consume()
    # file_transfer_del.consume()

    # asyncio.get_event_loop().run_until_complete(file_transfer_put('qiqiu5://tmp_file_pigcount-202306/ebcadbfe0fdd11ee96d300155d923235.jpg', 'pigcount-202306', 'ebcadbfe0fdd11ee96d300155d923235.jpg', -1))

    loop = asyncio.new_event_loop()
    loop.run_until_complete(extra_tasks())
    # asyncio.get_event_loop().run_until_complete(hmfs_client.cleanup_cloud())