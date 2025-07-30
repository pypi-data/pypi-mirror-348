from abc import ABC, abstractmethod
from typing import Any, Dict

import pymemcache
import redis


class Cache(ABC):
    client: pymemcache.Client | redis.Redis

    @classmethod
    @abstractmethod
    def from_config(cls, engine_config: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def get_json(self, key: str) -> Any | None:
        # TODO This method must also carry out ObjectId conversion!
        pass

    @abstractmethod
    def get_string(self, key: str) -> str | None:
        pass

    @abstractmethod
    def get_object(self, key: str) -> Any | None:
        pass

    @abstractmethod
    def set_json(self, key: str, value: Any) -> None:
        # TODO This method must also carry out ObjectId conversion!
        pass

    @abstractmethod
    def set_string(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def set_object(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass
