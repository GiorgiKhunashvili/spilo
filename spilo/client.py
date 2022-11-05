import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(kw_only=True)
class BaseClient(ABC):

    client_id: str = uuid.uuid4()
    
    @abstractmethod
    async def send(self, data: bytes | str):
        pass

    @abstractmethod
    async def close(self):
        pass

