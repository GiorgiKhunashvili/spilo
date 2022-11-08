import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass(kw_only=True)
class BaseClient(ABC):
    
    client_id: uuid.UUID = uuid.uuid4()

    def __hash__(self):
        return self.client_id.int

    @abstractmethod
    async def send(self, data: bytes | str):
        pass

    @abstractmethod
    async def close(self):
        pass

