"""The main app class for TacoBI."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import TypeVar
from uuid import UUID

from apscheduler.triggers.base import BaseTrigger

from tacobi.data_model.models import DataModelType
from tacobi.data_source import CachedDataSource, DataSourceManager
from tacobi.view import MaterializedView, View, ViewManager

T = TypeVar("T", bound=Callable[[DataModelType], Awaitable[DataModelType]])


@dataclass
class TacoBIApp:
    """The main app class for TacoBI."""

    view_manager: ViewManager
    """ Manager used for scheduling views."""

    data_source_manager: DataSourceManager = field(default_factory=DataSourceManager)
    """ Manager used for scheduling data sources."""

    _view_name_ids: dict[str, UUID] = field(default_factory=dict)
    """ A dictionary of view names. """

    # Data Source Management

    def data_source(
        self,
        name: str,
        trigger: BaseTrigger,
    ) -> Callable[
        [Callable[[DataModelType | None], Awaitable[DataModelType]]],
        Callable[[], DataModelType | None],
    ]:
        """Register a data source.

        Also transforms the function into a synchronous getter of the latest data.

        ### Arguments:
        - name: The name of the data source.
        - trigger: The trigger that will be used to schedule the data source.

        ### Returns:
        A function that returns the latest data from the data source.
        """

        def wrapper(
            func: Callable[[DataModelType | None], Awaitable[DataModelType]],
        ) -> Callable[[], DataModelType | None]:
            data_source = CachedDataSource(name=name, function=func, trigger=trigger)
            self.data_source_manager.add_data_source(data_source)

            return data_source.get_latest_data

        return wrapper

    # View Management

    def view(
        self,
        name: str | None = None,
        route: str | None = None,
        dependencies: list[Callable | str] | None = None,
    ) -> Callable[[T], T]:
        """Register a view.

        ### Arguments:
        - name: The name of the view.
        - route: The route of the view.
        - dependencies: The dependencies of the view.

        ### Returns:
        The view function itself.
        """

        def wrapper(
            func: Callable[[T], Awaitable[DataModelType]],
        ) -> Callable[[T], Awaitable[DataModelType]]:
            # Get the name
            view_name = name or func.__name__

            # Check that the name is unique:
            if view_name in self._view_name_ids:
                msg = f"View {view_name} already exists"
                raise ValueError(msg)

            # Convert the dependencies to names (as they could be strings or functions)
            dependency_names = (
                [dep if isinstance(dep, str) else dep.__name__ for dep in dependencies]
                if dependencies
                else []
            )

            # Get the dependencies
            try:
                dep_ids = (
                    [self._view_name_ids[dep] for dep in dependency_names]
                    if dependency_names
                    else []
                )
            except KeyError as e:
                msg = f"""Dependency {e} not found. Available dependencies:
                {self._view_name_ids.keys()}"""
                raise ValueError(msg) from e

            # Add the view to the view manager
            view = View(
                name=view_name,
                function=func,
                route=route,
                dependencies=dep_ids,
            )
            self.view_manager.add_view(view)

            # Register the view function in the view manager
            self._view_name_ids[view_name] = view.id

            # Return the view function
            return func

        return wrapper

    def materialized_view(
        self,
        name: str | None = None,
        route: str | None = None,
        dependencies: list[Callable | str] | None = None,
    ) -> Callable[
        [Callable[[DataModelType | None], Awaitable[DataModelType]]],
        Callable[[], DataModelType | None],
    ]:
        """Register a materialized view.

        Also transforms the function into a synchronous getter of the latest data.

        ### Arguments:
        - name: The name of the materialized view. If not provided, the name of the
          function will be used.
        - route: The route of the materialized view.
        - dependencies: The dependencies of the materialized view.

        ### Returns:
        A non-async function that returns the latest data from the materialized view.
        """

        def wrapper(
            func: Callable[[DataModelType | None], Awaitable[DataModelType]],
        ) -> Callable[[], DataModelType | None]:
            # Get the name
            view_name = name or func.__name__

            # Check that the name is unique:
            if view_name in self._view_name_ids:
                msg = f"Materialized view {view_name} already exists"
                raise ValueError(msg)

            # Convert the dependencies to names (as they could be strings or functions)
            dependency_names = (
                [dep if isinstance(dep, str) else dep.__name__ for dep in dependencies]
                if dependencies
                else []
            )

            # Get the dependency IDs
            try:
                dep_ids = (
                    [self._view_name_ids[dep] for dep in dependency_names]
                    if dependency_names
                    else []
                )
            except KeyError as e:
                msg = f"""Dependency {e} not found. Available dependencies:
                {self._view_name_ids.keys()}"""
                raise ValueError(msg) from e

            # Add the view to the view manager
            view = MaterializedView(
                name=view_name,
                function=func,
                route=route,
                dependencies=dep_ids,
            )
            self.view_manager.add_materialized_view(view)

            # Register the view function in the view manager
            self._view_name_ids[view_name] = view.id

            # Return the latest data from the view
            def _inner_func() -> DataModelType | None:
                return view.latest_data

            _inner_func.__name__ = view_name
            return _inner_func

        return wrapper

    # Lifecycle

    async def start(self) -> None:
        """Start the recomputation of datasets and materialized views."""
        await self.data_source_manager.start()
        await self.view_manager.start()

    async def stop(self) -> None:
        """Stop the recomputation of datasets and materialized views."""
        await self.data_source_manager.stop()
        self.view_manager.stop()
