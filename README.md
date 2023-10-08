# SPILO

Spilo is lightweight library for developing real time applications which helps developers managing websocket clients effectively and gives ability to scale horizontaly for handling large amount of clients.

## Installation


```console
$ pip install spilo
```


Here's example of the backend code for a simple websocket server:

**server.py**


```python
from typing import Dict
from dataclasses import dataclass
from fastapi import FastAPI, WebSocket

from spilo.channel import Channel
from spilo.base_client import BaseClient
from spilo.redis_pubsub import RedisPubSub
from spilo.event_registry import EventRegistry

app = FastAPI()
redis_pubsub = RedisPubSub()
redis_pubsub.connect()
event_registry = EventRegistry(event_key_name="event_type")


@dataclass
class Client(BaseClient):

    protocol: WebSocket

    def __hash__(self):
        return self.client_id.int

    async def send(self, data):
        await self.protocol.send_text(str(data))

    async def close(self):
        await self.protocol.close()

    async def listen(self):
        return await self.protocol.receive_text()


@app.websocket("/ws/{channel_name}")
async def websocket_endpoint(websocket: WebSocket, channel_name: str):
    await websocket.accept()
    client = Client(protocol=websocket)
    channel = Channel.get(channel_name, redis_pubsub, event_registry)
    channel.add_client(client)
    await channel.listen_client(client)


@event_registry.on("test")
async def test_event_handler(data: Dict, client: BaseClient, channel: Channel):
    await client.send(str(data))
    await channel.publish({"event_type": "test", "data": "test_data"})
```
