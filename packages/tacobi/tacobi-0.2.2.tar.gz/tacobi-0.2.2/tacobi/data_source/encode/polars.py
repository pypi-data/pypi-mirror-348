"""Encoders for Polars data."""

import io
from dataclasses import dataclass

import polars as pl

from tacobi.data_source.encode import EncodedDataType, Encoder


@dataclass
class PolarsEncoder(Encoder):
    """An encoder that can encode and decode Polars data."""

    def encode(self, data: pl.LazyFrame) -> EncodedDataType:
        """Encode the data."""
        buffer = io.BytesIO()
        data.sink_parquet(buffer)
        return buffer.getvalue()

    def decode(self, data: EncodedDataType) -> pl.LazyFrame:
        """Decode the data."""
        return pl.scan_parquet(io.BytesIO(data))
