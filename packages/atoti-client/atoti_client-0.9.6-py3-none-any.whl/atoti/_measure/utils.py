from collections.abc import Collection, Mapping
from typing import Any, cast

from py4j.java_gateway import JavaObject

from .._identification import (
    ColumnIdentifier,
    DimensionIdentifier,
    HasIdentifier,
    HierarchyIdentifier,
    LevelIdentifier,
    MeasureIdentifier,
    TableIdentifier,
)
from .._java_api import JavaApi
from .._measure_convertible import MeasureConvertible
from .._measure_definition import MeasureDefinition, convert_to_measure_definition
from .._operation import Condition, Operation
from .._py4j_utils import to_java_object, to_java_object_array


def get_measure_name(
    *,
    java_api: JavaApi,
    measure: MeasureDefinition,
    cube_name: str,
) -> str:
    """Get the name of the measure from either a measure or its name."""
    return measure._distil(java_api=java_api, cube_name=cube_name).measure_name


def _convert_plugin_measure_arg(
    *,
    java_api: JavaApi,
    arg: object,
) -> object:
    if isinstance(arg, HasIdentifier):
        return _extract_identifier(arg, java_api=java_api)

    # Recursively convert nested args.
    if isinstance(arg, tuple):
        return to_java_object_array(
            convert_plugin_measure_args(java_api=java_api, args=arg),
            gateway=java_api.gateway,
        )
    if isinstance(arg, list):
        return convert_plugin_measure_args(java_api=java_api, args=arg)
    if isinstance(arg, Mapping):
        return {
            _convert_plugin_measure_arg(
                java_api=java_api,
                arg=key,
            ): _convert_plugin_measure_arg(java_api=java_api, arg=value)
            for key, value in arg.items()
        }

    # Nothing smarter to do. Transform the argument to a java array.
    return to_java_object(arg, gateway=java_api.gateway)


def _extract_identifier(arg: HasIdentifier[Any], /, *, java_api: JavaApi) -> object:
    arg_identifier = arg._identifier

    if isinstance(arg_identifier, MeasureIdentifier):
        return arg_identifier.measure_name

    if isinstance(arg_identifier, ColumnIdentifier):
        return create_store_field(arg_identifier, java_api=java_api)

    if isinstance(arg_identifier, TableIdentifier):
        return arg_identifier.table_name

    if isinstance(arg_identifier, LevelIdentifier):
        return create_level_identifier(arg_identifier, java_api=java_api)

    if isinstance(arg_identifier, HierarchyIdentifier):
        return create_hierarchy_identifier(arg_identifier, java_api=java_api)

    if isinstance(arg_identifier, DimensionIdentifier):
        return arg_identifier.dimension_name

    raise TypeError(f"Unsupported identifier type: {type(arg_identifier)}")


def create_level_identifier(
    level: LevelIdentifier, /, *, java_api: JavaApi
) -> JavaObject:
    jvm: Any = java_api.gateway.jvm
    extension_package = jvm.io.atoti.runtime.internal.extension.util
    return extension_package.IdentifierFactory.createLevelIdentifierFromDescription(
        level._java_description
    )


def create_hierarchy_identifier(
    hierarchy: HierarchyIdentifier, /, *, java_api: JavaApi
) -> JavaObject:
    jvm: Any = java_api.gateway.jvm
    extension_package = jvm.io.atoti.runtime.internal.extension.util
    return extension_package.IdentifierFactory.createHierarchyIdentifierFromDescription(
        hierarchy._java_description
    )


def create_store_field(column: ColumnIdentifier, /, *, java_api: JavaApi) -> JavaObject:
    table_name = column.table_identifier.table_name
    column_name = column.column_name
    jvm: Any = java_api.gateway.jvm
    extension_package = jvm.io.atoti.runtime.internal.extension.util
    return extension_package.IdentifierFactory.createStoreField(table_name, column_name)


def convert_plugin_measure_args(
    *,
    java_api: JavaApi,
    args: Collection[object],
) -> list[object]:
    """Convert arguments used for creating a measure in Java.

    The ``Measure`` arguments are replaced by their name, and other arguments are
    translated into Java-equivalent objects when necessary.
    """
    return [_convert_plugin_measure_arg(java_api=java_api, arg=a) for a in args]


def convert_measure_args(
    *,
    java_api: JavaApi,
    cube_name: str,
    args: Collection[object],
) -> list[object]:
    """Convert arguments used for creating a measure in Java.

    The ``Measure`` arguments are replaced by their name, and other arguments are
    translated into Java-equivalent objects when necessary.
    """
    return [
        _convert_measure_arg(java_api=java_api, cube_name=cube_name, arg=a)
        for a in args
    ]


def _convert_measure_arg(  # noqa: PLR0911
    *,
    java_api: JavaApi,
    cube_name: str,
    arg: object,
) -> object:
    if isinstance(arg, MeasureDefinition):
        return get_measure_name(java_api=java_api, measure=arg, cube_name=cube_name)

    if isinstance(arg, HasIdentifier) and isinstance(
        arg._identifier, MeasureIdentifier
    ):
        return arg._identifier.measure_name

    if isinstance(arg, Condition | Operation):
        return _convert_measure_arg(
            java_api=java_api,
            cube_name=cube_name,
            arg=convert_to_measure_definition(cast(MeasureConvertible, arg)),
        )

    # Recursively convert nested args.
    if isinstance(arg, tuple):
        return to_java_object_array(
            convert_measure_args(java_api=java_api, cube_name=cube_name, args=arg),
            gateway=java_api.gateway,
        )
    if isinstance(arg, list):
        return convert_measure_args(java_api=java_api, cube_name=cube_name, args=arg)
    if isinstance(arg, Mapping):
        return {
            _convert_measure_arg(
                java_api=java_api,
                cube_name=cube_name,
                arg=key,
            ): _convert_measure_arg(java_api=java_api, cube_name=cube_name, arg=value)
            for key, value in arg.items()
        }

    # Nothing smarter to do. Transform the argument to a java array.
    return to_java_object(arg, gateway=java_api.gateway)
