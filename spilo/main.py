from dataclasses import dataclass
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .channel import Channel
from .base_client import BaseClient
from .redis_pubsub import RedisPubSub
from .event_registry import EventRegistry

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


@event_registry.on("wuwaoba")
def handle_wuwaoba(client_id, data):
    print("GMERTIIII \n\n\n\n")