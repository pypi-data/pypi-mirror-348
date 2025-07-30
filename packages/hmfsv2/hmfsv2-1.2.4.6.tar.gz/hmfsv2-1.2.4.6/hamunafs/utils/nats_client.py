import orjson
import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
from hamunafs.utils.singleton_wrapper import Singleton

class NATSClient(Singleton):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def connect(self):
        self.client = await nats.connect('nats://{}:{}@{}:{}'.format(self.username, self.password, self.host, self.port))

    async def publish(self, topic, params):
        if isinstance(params, str):
            _params = params.encode()
        else:
            _params = orjson.dumps(params)
        await self.client.publish(topic, _params)

    async def subscribe(self, topic, func):
        return await self.client.subscribe(topic, cb=func)

async def test_sub(msg):
    print(msg)
    
if __name__ == '__main__':

    
    client = NATSClient('gateway.ai.hamuna.club', 4222, 'hmcz', 'hmcz1234')

    loop = asyncio.get_event_loop()

    loop.run_until_complete(client.connect())
    if client.client.is_connected:
        sub = loop.run_until_complete(client.subscribe('test', test_sub))
        
        loop.run_until_complete(client.publish('test', 'hi'))

    import time
    while True:
        time.sleep(2)