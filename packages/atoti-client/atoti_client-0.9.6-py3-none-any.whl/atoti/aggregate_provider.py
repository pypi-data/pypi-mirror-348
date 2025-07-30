from __future__ import annotations

from typing import Annotated, Literal, TypeAlias, final

from pydantic import Field
from pydantic.dataclasses import dataclass

from ._collections import FrozenSequence
from ._constant import Scalar
from ._identification import Identifiable, LevelIdentifier, MeasureIdentifier
from ._operation import IsInCondition, LogicalCondition, RelationalCondition
from ._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG

_AggregateProviderLeafFilter: TypeAlias = (
    IsInCondition[LevelIdentifier, Literal["IS_IN"], Scalar]
    | RelationalCondition[LevelIdentifier, Literal["EQ"], Scalar]
)
_AggregateProviderFilter: TypeAlias = (
    _AggregateProviderLeafFilter
    | LogicalCondition[_AggregateProviderLeafFilter, Literal["AND"]]
)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class AggregateProvider:
    """An aggregate provider pre-aggregates some table columns up to certain levels.

    If a step of a query uses a subset of the aggregate provider's levels and measures, the provider will speed up the query.

    An aggregate provider uses additional memory to store the intermediate aggregates.
    The more levels and measures are added, the more memory it requires.

    Example:
        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        >>> df = pd.DataFrame(
        ...     {
        ...         "Seller": ["Seller_1", "Seller_1", "Seller_2", "Seller_2"],
        ...         "ProductId": ["aBk3", "ceJ4", "aBk3", "ceJ4"],
        ...         "Price": [2.5, 49.99, 3.0, 54.99],
        ...     }
        ... )
        >>> table = session.read_pandas(df, table_name="Seller")
        >>> cube = session.create_cube(table)
        >>> l, m = cube.levels, cube.measures
        >>> cube.aggregate_providers["Seller provider"] = tt.AggregateProvider(
        ...     key="bitmap",
        ...     levels=[l["Seller"], l["ProductId"]],
        ...     measures=[m["Price.SUM"]],
        ...     filter=l["ProductId"] == "cdJ4",
        ...     partitioning="modulo4(Seller)",
        ... )
        >>> cube.aggregate_providers
        {'Seller provider': AggregateProvider(key='bitmap', measures=(m['Price.SUM'],), levels=(l['Seller', 'Seller', 'Seller'], l['Seller', 'ProductId', 'ProductId']), filter=l['Seller', 'ProductId', 'ProductId'] == 'cdJ4', partitioning='modulo4(Seller)')}

    """

    key: Literal["bitmap", "leaf"] = "leaf"
    """The key of the provider.

    The bitmap is generally faster but also takes more memory.
    """

    measures: Annotated[
        FrozenSequence[Identifiable[MeasureIdentifier]],
        Field(min_length=1),
    ]
    """The measures to build the provider on."""

    levels: FrozenSequence[Identifiable[LevelIdentifier]] = ()
    """The levels to build the provider on."""

    filter: _AggregateProviderFilter | None = None
    """Only compute and provide aggregates matching this condition.

    The levels used in the condition do not have to be part of this provider's *levels*.
    """

    partitioning: str | None = None
    """The partitioning of the provider.

    Default to the partitioning of the cube's fact table.
    """
