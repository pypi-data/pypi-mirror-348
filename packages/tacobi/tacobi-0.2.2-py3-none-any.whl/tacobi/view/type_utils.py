"""Type utilities for extracting types from type annotations."""

import inspect
from collections.abc import Callable
from typing import TypeVar, get_args, get_origin, get_type_hints

T = TypeVar("T")
U = TypeVar("U")


def extract_return_type(func: Callable) -> type:
    """Extract the return type annotation from a function.

    ### Arguments:
    - func: The function to inspect

    ### Returns:
    The return type annotation

    ### Raises:
    - TypeError: If the function has no return type annotation
    """
    return_type = get_type_hints(func).get("return")
    if return_type is None:
        msg = "Function has no return type annotation"
        raise TypeError(msg)
    return return_type


def extract_container_type(container_type: type, expected_container_type: type) -> type:
    """Extract and validate the container type from a type annotation.

    ### Arguments:
    - container_type: The container type annotation
    - expected_container_type: The expected container type (e.g., DataFrame)

    ### Returns:
    The validated container type

    ### Raises:
    - TypeError: If the container type is not the expected type
    """
    origin = get_origin(container_type)
    if not isinstance(origin, type(expected_container_type)):
        msg = f"Expected {expected_container_type.__name__}, got {origin}"
        raise TypeError(msg)
    return origin


def extract_container_content(
    container_type: type, expected_container_type: type, content_type: type
) -> type:
    """Extract the content type from a container type annotation.

    ### Arguments:
    - container_type: The container type annotation
    - expected_container_type: The expected container type (e.g., DataFrame)
    - content_type: The expected base class of the content (e.g., DataFrameModel)

    ### Returns:
    The content type used in the container type annotation

    ### Raises:
    - TypeError: If the container type is not properly formatted
    """
    # Check if it's the expected container type
    extract_container_type(container_type, expected_container_type)

    # Extract the model from Container[Model]
    type_args = get_args(container_type)
    if not type_args or len(type_args) != 1:
        msg = f"{expected_container_type.__name__} must have exactly one type argument. Actual: {type_args}"
        raise TypeError(msg)

    content_class = type_args[0]

    # Verify it's the expected content type
    if not (inspect.isclass(content_class) and issubclass(content_class, content_type)):
        msg = f"Expected {content_type.__name__}, got {content_class}."
        raise TypeError(msg)

    return content_class


def extract_model_from_typehints(
    func: Callable, expected_container_type: type, expected_model_base: type
) -> type:
    """Extract a model class from a function that returns Container[Model].

    ### Arguments:
    - func: The function to inspect
    - expected_container_type: The expected container type (e.g., DataFrame)
    - expected_model_base: The expected base class of the model (e.g., DataFrameModel)

    ### Returns:
    The model class used in the container type annotation

    ### Raises:
    - TypeError: If the function's return type is not properly annotated
    """
    return_type = extract_return_type(func)
    return extract_container_content(
        return_type, expected_container_type, expected_model_base
    )
