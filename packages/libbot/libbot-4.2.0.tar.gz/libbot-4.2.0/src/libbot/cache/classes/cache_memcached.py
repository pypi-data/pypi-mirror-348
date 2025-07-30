import logging
from logging import Logger
from typing import Dict, Any, Optional

from pymemcache import Client

from .cache import Cache
from ..utils._objects import _json_to_string, _string_to_json

logger: Logger = logging.getLogger(__name__)


class CacheMemcached(Cache):
    client: Client

    def __init__(self, client: Client, prefix: Optional[str] = None):
        self.client: Client = client
        self.prefix: str | None = prefix

        logger.info("Initialized Memcached for caching")

    @classmethod
    def from_config(cls, engine_config: Dict[str, Any], prefix: Optional[str] = None) -> "CacheMemcached":
        if "uri" not in engine_config:
            raise KeyError(
                "Cache configuration is invalid. Please check if all keys are set (engine: memcached)"
            )

        return cls(Client(engine_config["uri"], default_noreply=True), prefix=prefix)

    def _get_prefixed_key(self, key: str) -> str:
        return key if self.prefix is None else f"{self.prefix}_{key}"

    def get_json(self, key: str) -> Any | None:
        key = self._get_prefixed_key(key)

        try:
            result: Any | None = self.client.get(key, None)

            logger.debug(
                "Got json cache key '%s'%s",
                key,
                "" if result is not None else " (not found)",
            )
        except Exception as exc:
            logger.error("Could not get json cache key '%s' due to: %s", key, exc)
            return None

        return None if result is None else _string_to_json(result)

    def get_string(self, key: str) -> str | None:
        key = self._get_prefixed_key(key)

        try:
            result: str | None = self.client.get(key, None)

            logger.debug(
                "Got string cache key '%s'%s",
                key,
                "" if result is not None else " (not found)",
            )

            return result
        except Exception as exc:
            logger.error("Could not get string cache key '%s' due to: %s", key, exc)
            return None

    # TODO Implement binary deserialization
    def get_object(self, key: str) -> Any | None:
        raise NotImplementedError()

    def set_json(self, key: str, value: Any) -> None:
        key = self._get_prefixed_key(key)

        try:
            self.client.set(key, _json_to_string(value))
            logger.debug("Set json cache key '%s'", key)
        except Exception as exc:
            logger.error("Could not set json cache key '%s' due to: %s", key, exc)
            return None

    def set_string(self, key: str, value: str) -> None:
        key = self._get_prefixed_key(key)

        try:
            self.client.set(key, value)
            logger.debug("Set string cache key '%s'", key)
        except Exception as exc:
            logger.error("Could not set string cache key '%s' due to: %s", key, exc)
            return None

    # TODO Implement binary serialization
    def set_object(self, key: str, value: Any) -> None:
        raise NotImplementedError()

    def delete(self, key: str) -> None:
        key = self._get_prefixed_key(key)

        try:
            self.client.delete(key)
            logger.debug("Deleted cache key '%s'", key)
        except Exception as exc:
            logger.error("Could not delete cache key '%s' due to: %s", key, exc)
