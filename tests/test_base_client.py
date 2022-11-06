# from dataclasses import dataclass
#
# from spilo.base_client import BaseClient
# from spilo.channel import Channel
#
#
# def test_overiding_id_field_in_base_client():
#
#     @dataclass
#     class Client(BaseClient):
#
#         client_id: str
#         __hash__ = BaseClient.__hash__
#
#         async def send(self, data):
#             pass
#
#         async def close(self):
#             pass
#
#     client = Client("test_client_id")
#     channel = Channel("test_channel")
#
#     assert client.client_id == "test_client_id"
#     assert client.__hash__ is not None
#
#     channel.add_client(client)
#
#     assert len(channel.clients) == 1
#
