import pytest

from spilo.base_client import BaseClient


class Client(BaseClient):

    async def send(self, data):
        pass

    async def close(self):
        pass


@pytest.fixture
def client():
    c = Client()
    yield c

