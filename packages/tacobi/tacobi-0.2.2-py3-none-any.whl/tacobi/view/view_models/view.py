"""Views."""

from dataclasses import dataclass
from typing import Generic

from tacobi.data_model.models import DataModelType
from tacobi.view.view_models.base import BaseView


@dataclass
class View(BaseView, Generic[DataModelType]):
    """A standard view."""
