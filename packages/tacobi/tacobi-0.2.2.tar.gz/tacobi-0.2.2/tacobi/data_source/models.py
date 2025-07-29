"""Models for data sources."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Generic

import polars as pl
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.base import BaseTrigger
from pydantic import BaseModel

from tacobi.data_model.models import DataModelType
from tacobi.data_source.cache import CacheBackend, SQLiteCache
from tacobi.data_source.encode import Encoder, PolarsEncoder, PydanticEncoder


@dataclass
class CachedDataSource(Generic[DataModelType]):
    """A data source that is locally stored and can be instantly queried."""

    name: str
    """ The *UNIQUE* name of the data source. """

    function: Callable[[DataModelType | None], Awaitable[DataModelType]]
    """ The function that is used to update the data. """

    trigger: BaseTrigger
    """ The cron trigger that is used to update the data source. """

    _encoder: Encoder | None = None
    """ The encoder that is used to encode and decode the data. """

    _cached_data: DataModelType | None = None
    """ Latest cached data, None if no data has been cached yet. """

    _cache_backend: CacheBackend | None = None
    """ The cache backend that is used to store the data. """

    def __post_init__(self) -> None:
        """Based on the type hints for the function, determine the encoder."""
        return_type = self.function.__annotations__["return"]
        if issubclass(return_type, pl.LazyFrame) or return_type == pl.LazyFrame:
            self._encoder = PolarsEncoder()
        elif issubclass(return_type, BaseModel):
            self._encoder = PydanticEncoder(base_model=return_type)
        else:
            msg = f"No encoder found for type {return_type}"
            raise RuntimeError(msg)

    def set_cache_backend(self, cache_backend: CacheBackend) -> None:
        """Set the cache backend that is used to store the data."""
        self._cache_backend = cache_backend

    async def update(self) -> None:
        """Call the fetch function and update the cache accordingly."""
        if not self._cache_backend:
            msg = "Cache backend not set"
            raise RuntimeError(msg)

        self._cached_data = await self.function(self._cached_data)

        await self._cache_backend.set(
            key=self.name, value=self._encoder.encode(self._cached_data)
        )

    async def load(self) -> None:
        """Load the data from the cache backend."""
        if not self._cache_backend:
            msg = "Cache backend not set"
            raise RuntimeError(msg)

        cache_data = await self._cache_backend.get(key=self.name)
        if cache_data is None:
            return
        self._cached_data = self._encoder.decode(cache_data)

    def get_latest_data(self) -> DataModelType | None:
        """Get the latest data from the data source."""
        data = self._cached_data
        if data is None:
            return None
        return data


# Scheduler


@dataclass
class DataSourceManager:
    """A manager that can schedule data sources to be updated at a specific time."""

    cache_backend: CacheBackend = field(default_factory=SQLiteCache)
    """ The cache backend that is used to store the data. """

    _data_sources: list[CachedDataSource] = field(default_factory=list)
    """ The data sources that are scheduled to be updated. """

    _scheduler: AsyncIOScheduler = field(default_factory=AsyncIOScheduler)
    """ The scheduler that is used to schedule the tasks. """

    # Data Source Scheduling

    def _schedule_data_source(self, data_source: CachedDataSource) -> None:
        """Schedule a data source to be updated according to its trigger.

        ### Arguments
        - data_source: The data source to schedule.
        """

        async def update_job() -> None:
            await data_source.update()

        self._scheduler.add_job(
            update_job,
            trigger=data_source.trigger,
            id=f"update_{data_source.name}",
            replace_existing=True,
        )

    def add_data_source(self, data_source: CachedDataSource) -> None:
        """Add a data source to the scheduler."""
        data_source.set_cache_backend(self.cache_backend)
        self._data_sources.append(data_source)
        self._schedule_data_source(data_source)

    # Lifecycle

    async def start(self) -> None:
        """Start the scheduler."""
        for data_source in self._data_sources:
            await data_source.load()
        self._scheduler.start()

    async def stop(self) -> None:
        """Stop the scheduler."""
        self._scheduler.shutdown()
        await self.cache_backend.cleanup()
