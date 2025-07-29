"""Models for data sources."""

from abc import ABC, abstractmethod

from tacobi.data_model.models import DataModelType

EncodedDataType = bytes


class Encoder(ABC):
    """An encoder that can encode and decode data."""

    @abstractmethod
    def encode(self, data: DataModelType) -> EncodedDataType:
        """Encode the data."""
        ...

    @abstractmethod
    def decode(self, data: EncodedDataType) -> DataModelType:
        """Decode the data."""
        ...
