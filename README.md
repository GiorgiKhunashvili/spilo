# SPILO

Spilo is lightweight library for developing real time applications which helps developers managing websocket clients effectively and gives ability to scale horizontaly for handling large amount of clients.

## Installation


```console
$ pip install spilo
```


Here's example of the backend code for a simple websocket server:

**server.py**


```python
from dataclasses import dataclass
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from spilo.channel import Channel
from spilo.base_client import BaseClient
from spilo.redis_pubsub import RedisPubSub

app = FastAPI()
redis_pubsub = RedisPubSub()
redis_pubsub.connect()


@dataclass
class Client(BaseClient):

    protocol: WebSocket

    def __hash__(self):
        return self.client_id.int

    async def send(self, data):
        await self.protocol.send_text(str(data))

    async def close(self):
        await self.protocol.close()


@app.websocket("/ws/{channel_name}")
async def websocket_endpoint(websocket: WebSocket, channel_name: str):
    await websocket.accept()
    client = Client(protocol=websocket)
    channel = Channel.get(channel_name, redis_pubsub)
    channel.add_client(client)
    try:
        while True:
            data = await websocket.receive_text()
            await channel.publish(data)
    except WebSocketDisconnect:
        channel.remove_client(client)
```
