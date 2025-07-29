"""Base view class."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Generic
from uuid import UUID, uuid4

from pandera.polars import DataFrameModel
from pandera.typing.polars import DataFrame
from pydantic import BaseModel

from tacobi.data_model.models import DataModelType
from tacobi.view.type_utils import (
    extract_container_type,
    extract_model_from_typehints,
    extract_return_type,
)
from tacobi.view.view_models.endpoint_model import (
    ViewEndpointResponseModel,
    create_column_base_model_from_dataframe_model,
)


@dataclass
class BaseView(Generic[DataModelType]):
    """Base view class."""

    function: Callable[..., Awaitable[DataModelType]]
    """The function to call to update the view."""

    dependencies: list[UUID] = field(default_factory=list)
    """The dependencies of the view used for topological sorting."""

    route: str | None = None
    """The optional REST route of the view."""

    name: str | None = None
    """The optional name of the view for logging and debugging."""

    id: UUID = field(default_factory=uuid4)
    """The unique identifier for the view."""

    def __str__(self) -> str:
        """Get the string representation of the view."""
        return f"View(name={self.name}, id={self.id})"

    def __hash__(self) -> int:
        """Hash the view."""
        return hash(self.id)

    # =====================================================
    # Pydantic BaseModel conversion
    # =====================================================

    @cached_property
    def return_type(self) -> type[DataModelType]:
        """The return type of the view."""
        return extract_return_type(self.function)

    @cached_property
    def base_model(self) -> tuple[type[BaseModel], bool]:
        """The base model of the view and whether it's a list (aka a DataFrameModel).

        ### Returns:
        A tuple of the base model and a boolean indicating whether it's a list.
        """
        # If it's already a BaseModel, we can return it directly
        if issubclass(self.return_type, BaseModel):
            return self.return_type, False

        # Otherwise, it's a DataFrameModel, so we need to wrap it in a list
        container_type = extract_container_type(self.return_type, DataFrame)
        model = extract_model_from_typehints(
            self.function, container_type, DataFrameModel
        )

        return create_column_base_model_from_dataframe_model(model), True

    @cached_property
    def fastapi_response_model(self) -> type[ViewEndpointResponseModel]:
        """The response model for the view.

        ### Returns:
        The response model for the view.
        """
        base_model, is_list = self.base_model
        model = base_model if not is_list else list[base_model]
        return ViewEndpointResponseModel.create_class_from_model(model)

    def convert_to_base_model(self, data: DataModelType) -> BaseModel | list[BaseModel]:
        """Convert data to BaseModel format.

        Called internally when generating the FastAPI response.

        ### Arguments:
        - data: Either a BaseModel instance or DataFrame to convert

        ### Returns:
        BaseModel instance or list of BaseModel instances
        """
        # If it's already a BaseModel, return it directly
        if isinstance(data, BaseModel):
            return data

        # Otherwise, assume it's a DataFrame and convert to list of BaseModels
        base_model_class, _ = self.base_model

        # Handle both pandas and polars DataFrames
        if hasattr(data, "to_dicts"):  # Polars
            records = data.to_dicts()
        else:  # Pandas
            records = data.to_dict("records")

        return [base_model_class(**row) for row in records]
