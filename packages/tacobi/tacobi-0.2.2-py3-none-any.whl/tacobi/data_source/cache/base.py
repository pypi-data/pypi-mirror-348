"""Base class for cache backends."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from tacobi.data_source.encode import EncodedDataType


@dataclass
class CacheBackend(ABC):
    """A cache backend that can be used to store and retrieve data."""

    @abstractmethod
    async def get(self, key: str) -> EncodedDataType | None:
        """Get the data for the given key.

        ### Arguments
        - key: The key to get the data for.

        ### Returns
        - The data for the given key, or None if the data is not found.
        """
        ...

    @abstractmethod
    async def set(self, key: str, value: EncodedDataType) -> None:
        """Set the data for the given key.

        ### Arguments
        - key: The key to set the data for.
        - data: The data to set.
        """
        ...

    @abstractmethod
    async def clear(self) -> None:
        """Clear the cache."""
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup the cache."""
        ...
