"""Models for data models."""

from typing import TypeVar

from pandera.typing.common import DataFrameBase
from pydantic import BaseModel

DataModel = DataFrameBase | BaseModel
"""A valid data model can either be a Pandera Polars `DataFrameModel` or a
Pydantic `BaseModel`. Views and data sources can return either of these types.
"""

DataModelType = TypeVar("DataModelType", bound=DataModel)
"""A type variable for the data model type."""
