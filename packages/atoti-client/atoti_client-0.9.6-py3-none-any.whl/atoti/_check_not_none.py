# Revisit the need for these functions once https://github.com/graphql/graphql-wg/pull/772 is supported by Spring for GraphQL and ariadne-codegen.

from typing import Literal, TypeAlias, TypeVar

_ErrorType: TypeAlias = type[KeyError] | type[RuntimeError]


_T = TypeVar("_T")


def check_data_model_not_none(
    data_model: _T | None,
    /,
    *,
    data_model_transaction_id: str | None,
    error_type: _ErrorType = RuntimeError,
) -> _T:
    if data_model is None:
        if data_model_transaction_id is None:
            raise AssertionError("There should always be a main data model.")

        raise error_type(
            f"No data model with transaction id: `{data_model_transaction_id}`."
        )

    return data_model


def _check_named_object_not_none(
    value: _T | None,
    type_name: str,
    name: str,
    /,
    *,
    error_type: _ErrorType,
) -> _T:
    if value is None:
        raise error_type(f"No {type_name} named `{name}`.")

    return value


def check_named_object_not_none(
    value: _T | None,
    # The `Literal` provides autocomplete and prevent typos, feel free to add new strings as needed.
    type_name: Literal[
        "column",
        "cube",
        "dimension",
        "hierarchy",
        "level",
        "measure",
        "query cube",
        "table",
    ],
    name: str,
    /,
    *,
    error_type: _ErrorType = RuntimeError,
) -> _T:
    """Check that *value* is not ``None`` and return it.

    When ``value`` is ``None``, this function raises an informative error message mentioning both **type_name** and **name**.
    It provides a better UX than ``assert value is not None`` (and also raises even when ``assert``s are disabled).
    """
    return _check_named_object_not_none(
        value,
        type_name,
        name,
        error_type=error_type,
    )
