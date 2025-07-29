"""Dataset schema classes."""

from collections.abc import Callable, Iterable
from datetime import datetime
from enum import Enum
from typing import Any, Generic, Self, TypeVar, get_args, get_origin

from pandera import Column, DataFrameModel
from pandera.dtypes import DataType, is_numeric, is_string
from pandera.typing.common import DataFrameBase
from pydantic import BaseModel, Field, create_model

DataFrameBaseT = TypeVar("DataFrameBaseT", bound=DataFrameBase)
DatasetFunctionType = Callable[[], DataFrameBaseT]


# Transforming DataFrameModel to BaseModel


class ValueTypeEnum(str, Enum):
    """The type of a value in a column. Used for fabricating Pydantic models."""

    STRING = "string"
    NUMBER = "number"

    @classmethod
    def from_pandera_dtype(cls, dtype: DataType) -> "ValueTypeEnum":
        """Convert a pandera dtype to a ValueTypeEnum."""
        if is_numeric(dtype):
            return cls.NUMBER
        if is_string(dtype):
            return cls.STRING
        msg = f"Unsupported dtype: {dtype}"
        raise ValueError(msg)

    def into_python_type(self) -> type[str] | type[float]:
        """Convert a ValueTypeEnum to a Python type."""
        match self:
            case self.STRING:
                return str
            case self.NUMBER:
                return float
            case _:
                msg = f"Unsupported value type: {self}"
                raise ValueError(msg)


def create_column_base_model_from_dataframe_model(
    dataframe_model: type[DataFrameModel],
) -> type[BaseModel]:
    """Create a BaseModel from a DataFrameModel.

    ### Arguments:
    - dataframe_model: The DataFrameModel to create a BaseModel from.

    ### Returns:
    The BaseModel class.
    """
    schema_columns: Iterable[Column] = dataframe_model.to_schema().columns.values()
    fields: dict[str, tuple[type[Any], Any]] = {}
    for col in schema_columns:
        python_type = ValueTypeEnum.from_pandera_dtype(col.dtype).into_python_type()
        fields[col.name] = (python_type, Field(description=col.description))

    return create_model(f"{dataframe_model.__name__}Model", **fields)


# Response returned by all view endpoints

M = TypeVar("M", bound=BaseModel | list[BaseModel])


class ViewEndpointResponseModel(BaseModel, Generic[M]):
    """The return object of a view endpoint."""

    last_updated: datetime | None
    """The last updated date of the view."""

    data: M | None
    """The data of the view."""

    @classmethod
    def create_class_from_model(
        cls: type[Self], model: type[M]
    ) -> type["ViewEndpointResponseModel[M]"]:
        """Create a response wrapper class from a model.

        ### Arguments:
        - model: The model to create a response wrapper class from.

        ### Returns:
        The response wrapper class.
        """
        # If the model is NOT a list, we can just use its properties directly
        base_model = model
        name = base_model.__name__

        # If it is a list, we need to extract the base model from inside the list
        is_list = get_origin(model) is list
        if is_list:
            args = get_args(model)
            if len(args) != 1:
                msg = f"List model must have exactly one type argument, got {len(args)}"
                raise ValueError(msg)
            base_model = args[0]
            name = f"{base_model.__name__}List"

        fields = {
            "last_updated": (
                datetime | None,
                Field(description="The time the view was last updated at."),
            ),
            "data": (model | None, Field(description="The data of the view.")),
        }
        return create_model(
            f"{name}Response",
            **fields,
            __doc__=f"Response container model for {name} (data).",
        )
