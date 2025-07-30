import paho.mqtt.client as mqtt
import json
from threading import Thread

import uuid

from .singleton_wrapper import Singleton

from concurrent.futures import ThreadPoolExecutor
import asyncio


class MQTTClient(Singleton):
    def __init__(self, client_id, username, password, loop: asyncio.AbstractEventLoop=None):
        self.connected = False

        self.client = mqtt.Client(client_id=client_id + str(uuid.uuid1()), clean_session=True)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.username_pw_set(username, password)

        self.subscribes = []

        self.loop = loop

        if self.loop:
            self.executor = ThreadPoolExecutor(max_workers=8)

    def connect(self, host, port):
        self.thread = Thread(target=self.__mqtt_connect, args=(host, port))
        self.thread.setDaemon(True)
        self.thread.start()
        return self

    def subscribe(self, topic, qos):
        if self.connected:
            self.client.subscribe(topic, qos)
        self.subscribes.append((topic, qos))

    def register_on_message_handler(self, handler):
        self.on_message_handler = handler

    def join(self):
        if self.thread:
            self.thread.join()

    def __mqtt_connect(self, host, port):
        try:
            self.client.connect(host, port=port, keepalive=60)
            self.client.loop_forever()
        except Exception as e:
            print(e)

    def _on_connect(self, client, userdata, flags, rc):
        if not self.connected:
            self.connected = True
            print("mqtt service connected")
            
            for subscribe in self.subscribes:
                print('subscribing topic: {}/qos:{}...'.format(subscribe[0], subscribe[1]))
                self.client.subscribe(subscribe[0], subscribe[1])

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("mqtt service disconnected")

    def _on_message(self, client, userdata, msg):
        if self.on_message_handler:
            self.on_message_handler(client, userdata, msg)

    def _on_publish(self, client, userdata, msg):
        print('published')

    def publish(self, message, topic, retain=False, qos=0, expires=7200):
        if not isinstance(message, str):
            message = json.dumps(message)

        try:
            self.client.publish(topic, payload=message, retain=retain, qos=qos)
            return True
        except Exception as e:
            pass
        return False
            
    async def publish_async(self, message, topic, retain=False, qos=0, expires=7200):
        return await self.loop.run_in_executor(self.executor, self.publish, message, topic, retain, qos, expires)