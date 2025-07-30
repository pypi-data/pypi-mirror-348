from collections.abc import Callable, Sequence
from dataclasses import replace
from typing import Literal

import pandas as pd

from .._activeviam_client import ActiveViamClient
from .._context import Context
from .._cube_discovery import CubeDiscovery
from .._cube_query_filter_condition import CubeQueryFilterCondition
from .._generate_mdx import generate_mdx
from .._get_data_types import GetDataTypes
from .._identification import LevelIdentifier, MeasureIdentifier
from .._typing import Duration
from ..mdx_query_result import MdxQueryResult
from ._execute_mdx_query import execute_mdx_query


def execute_cube_query(
    *,
    activeviam_client: ActiveViamClient,
    context: Context,
    cube_name: str,
    filter: CubeQueryFilterCondition | None,  # noqa: A002
    get_cube_discovery: Callable[[], CubeDiscovery],
    get_data_types: GetDataTypes,
    get_widget_creation_code: Callable[[], str | None],
    has_data_export_service: bool,
    include_empty_rows: bool,
    include_totals: bool,
    level_identifiers: Sequence[LevelIdentifier],
    measure_identifiers: Sequence[MeasureIdentifier],
    mode: Literal["pretty", "raw"],
    pivot_namespace: str,
    scenario_name: str | None,
    session_id: str,
    timeout: Duration,
) -> pd.DataFrame:
    cube_discovery = get_cube_discovery()
    mdx_ast = generate_mdx(
        cube=cube_discovery.cubes[cube_name],
        filter=filter,
        include_empty_rows=include_empty_rows,
        include_totals=include_totals,
        level_identifiers=level_identifiers,
        measure_identifiers=measure_identifiers,
        scenario=scenario_name,
    )
    mdx = str(mdx_ast)

    query_result = execute_mdx_query(
        activeviam_client=activeviam_client,
        context=context,
        get_cube_discovery=lambda: cube_discovery,
        get_data_types=get_data_types,
        get_widget_creation_code=get_widget_creation_code,
        has_data_export_service=has_data_export_service,
        keep_totals=include_totals,
        mdx=mdx,
        mode=mode,
        pivot_namespace=pivot_namespace,
        session_id=session_id,
        timeout=timeout,
    )

    if (
        not include_totals
        and isinstance(query_result, MdxQueryResult)
        and query_result._atoti_metadata is not None
        and query_result._atoti_metadata.widget_conversion_details is not None
    ):
        mdx_ast = generate_mdx(
            cube=cube_discovery.cubes[cube_name],
            filter=filter,
            include_empty_rows=include_empty_rows,
            # Always use an MDX including totals because Atoti UI 5 relies only on context values to show/hide totals.
            include_totals=True,
            level_identifiers=level_identifiers,
            measure_identifiers=measure_identifiers,
            scenario=scenario_name,
        )
        mdx = str(mdx_ast)
        query_result._atoti_metadata = (
            query_result._atoti_metadata.add_widget_conversion_details(
                replace(
                    query_result._atoti_metadata.widget_conversion_details,
                    mdx=mdx,
                ),
            )
        )

    return query_result
