from itertools import chain, product
from typing import Literal, overload

from .operation import (
    ConditionBound,
    LogicalCondition,
    LogicalConditionLeafOperandBound,
    LogicalConditionLeafOperandT_co,
    LogicalConditionOperatorBound,
)


@overload
def disjunctive_normal_form_from_condition(
    condition: LogicalConditionLeafOperandT_co,  # type: ignore[misc]
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co]]: ...


@overload
def disjunctive_normal_form_from_condition(  # type: ignore[overload-overlap] # pyright: ignore[reportOverlappingOverload]
    condition: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, Literal["AND"]],
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co, ...]]: ...


@overload
def disjunctive_normal_form_from_condition(
    condition: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, Literal["OR"]],
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co], ...]: ...


@overload
def disjunctive_normal_form_from_condition(
    condition: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, LogicalConditionOperatorBound],
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co], ...]: ...


def disjunctive_normal_form_from_condition(
    condition: ConditionBound,
    /,
) -> tuple[tuple[LogicalConditionLeafOperandBound, ...], ...]:
    """Decombine the passed condition into leave conditions in disjunctive normal form (DNF).

    For example: ``foo & (bar | baz)`` will return ``((foo, bar), (foo, baz))``.
    """
    if not isinstance(condition, LogicalCondition):
        return ((condition,),)

    disjunctive_normal_forms = [
        disjunctive_normal_form_from_condition(operand)
        for operand in condition.operands
    ]

    match condition.operator:
        case "AND":
            return tuple(
                tuple(chain.from_iterable(conditions))
                for conditions in product(*disjunctive_normal_forms)
            )
        case "OR":
            return tuple(chain.from_iterable(disjunctive_normal_forms))
