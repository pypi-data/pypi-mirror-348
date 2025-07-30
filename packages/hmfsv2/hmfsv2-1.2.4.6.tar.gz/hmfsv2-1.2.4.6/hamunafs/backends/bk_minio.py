import asyncio
import traceback
from aiohttp_retry import ExponentialRetry, RetryClient

from hamunafs.utils.minio_async import MinioAsync

from hamunafs.backends.base import BackendBase

class MinioBackend(BackendBase):
    def __init__(self, cfg):
        key, secret, domain, default_bucket = cfg['key'], cfg['secret'], cfg['domain'], cfg['default_bucket']
        self.client = MinioAsync(domain, key, secret, secure=False)
        self.domain = domain
        self.default_bucket = default_bucket
    
    def geturl(self, entrypoint):
        bucket, bucket_name = entrypoint.split('/')
        return 'http://{}/{}/{}_{}'.format(self.domain, self.default_bucket, bucket, bucket_name)

    async def put_async(self, file, bucket, bucket_name, tmp=True):
        try:
            if tmp:
                _bucket = 'tmp_file_' + bucket
            else:
                _bucket = bucket
            b_name = '{}_{}'.format(_bucket, bucket_name)
            print('uploading to {}...'.format(self.domain))
            ret, e = await asyncio.wait_for(self.client.upload_file(file, self.default_bucket, b_name), timeout=20)
            if ret:
                print('upload success.')
                return True, '{}/{}'.format(_bucket, bucket_name)
            print('upload failed: {}'.format(e))
            return False, e
        except Exception as e:
            return False, traceback.format_exc()

    async def put_buffer_async(self, buffer, bucket, bucket_name):
        try:
            b_name = '{}_{}'.format(bucket, bucket_name)
            ret, e = await asyncio.wait_for(self.client.upload_file_by_buffer(buffer, self.default_bucket, b_name), timeout=60)
            if ret is not None:
                return True, '{}/{}'.format(bucket, bucket_name)
            return False, '上传失败'
        except Exception as e:
            return False, str(e)

    async def get_async(self, download_path, bucket, bucket_name, tries=0):
        try:
            if tries >= 3:
                return False, '下载出错'
            else:
                url = 'http://{}/{}/{}'.format(self.domain, self.default_bucket, '{}_{}'.format(bucket, bucket_name))
                print('downloading {} -> {}'.format(url, download_path))

                # if os.path.isfile(download_path):
                #     os.remove(download_path)

                # self.create_dir_if_not_exists(download_path)
                # path = self.download_file(url, download_path)
                # if path:
                #     return True, download_path
                ret, e = await asyncio.wait_for(self.client.download_file(download_path, self.default_bucket, '{}_{}'.format(bucket, bucket_name)), timeout=60)
                if ret:
                    return True, e
                return await self.get_async(download_path, bucket, bucket_name, tries+1)
        except Exception as e:
            traceback.print_exc()
            if tries >= 3:
                return False, str(e)
            else:
                return await self.get_async(download_path, bucket, bucket_name, tries+1)


            
