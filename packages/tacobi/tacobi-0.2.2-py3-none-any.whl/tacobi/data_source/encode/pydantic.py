"""Encoders for Pydantic models."""

from dataclasses import dataclass
from typing import TypeVar

from pydantic import BaseModel

from tacobi.data_model.models import DataModelType
from tacobi.data_source.encode import EncodedDataType, Encoder

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


@dataclass
class PydanticEncoder(Encoder):
    """An encoder that can encode and decode Pydantic models."""

    base_model: BaseModelType
    """ The base model that is used to encode and decode the data. """

    def encode(self, data: DataModelType) -> EncodedDataType:
        """Encode the data."""
        return data.model_dump_json().encode("utf-8")

    def decode(self, data: EncodedDataType) -> DataModelType:
        """Decode the data."""
        return self.base_model.model_validate_json(data.decode("utf-8"))
