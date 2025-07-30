from collections.abc import Callable
from functools import wraps
from typing import Any, final

from py4j.protocol import Py4JError, Py4JJavaError


def enhance_py4j_errors(function: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Makes the given method eagerly evaluate error messages of uncaught ``Py4JJavaError``s."""

    @wraps(function)
    def wrapped_method(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except Py4JJavaError as java_exception:
            raise _AtotiJavaError(java_exception) from java_exception

    return wrapped_method


@final
class _AtotiJavaError(Py4JError):  # type: ignore[misc]
    def __init__(self, java_error: Py4JJavaError):
        super().__init__(str(java_error), cause=java_error)
