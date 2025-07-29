"""Materialized views."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Generic

from pydantic import BaseModel

from tacobi.data_model.models import DataModelType
from tacobi.view.view_models.base import BaseView


@dataclass
class MaterializedView(BaseView, Generic[DataModelType]):
    """A materialized view."""

    function: Callable[[], Awaitable[DataModelType]]
    """The function to call to update the view."""

    latest_update: datetime | None = None
    """The latest update of the view."""

    latest_data: DataModelType | None = None
    """The latest data from the view."""

    def __str__(self) -> str:
        """Get the string representation of the view."""
        return f"MaterializedView(name={self.name}, id={self.id})"

    @property
    def latest_data_as_base_model(self) -> BaseModel | list[BaseModel] | None:
        """Get the latest data from the view as a BaseModel.

        ### Returns:
        The latest data from the view as a BaseModel.
        """
        return (
            self.convert_to_base_model(self.latest_data)
            if self.latest_data is not None
            else None
        )

    async def recompute_latest_data(self) -> None:
        """Recompute the latest data from the view."""
        self.latest_data = await self.function()
        self.latest_update = datetime.now(UTC)

    def __hash__(self) -> int:
        """Hash the view."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Check if the view is equal to another object."""
        if not isinstance(other, MaterializedView):
            return False
        return self.id == other.id
