from __future__ import annotations

from .._doc import doc
from .._escape_literal_in_format_string import escape_literal_in_format_string
from .._experimental import experimental
from .._measure.irr import IrrMeasure
from .._measure_convertible import VariableMeasureConvertible
from .._measure_definition import MeasureDefinition, convert_to_measure_definition
from ..hierarchy import Hierarchy


@doc(
    formula=escape_literal_in_format_string(
        r"NPV = \sum_{i=0}^{T} CF_i (1 + r)^{\frac{T - t_i}{T}} = 0"
    )
)
@experimental()
def irr(
    *,
    cash_flows: VariableMeasureConvertible,
    market_value: VariableMeasureConvertible,
    date: Hierarchy,
    precision: float = 0.001,
) -> MeasureDefinition:
    r"""Return the Internal Rate of Return based on the underlying cash flows and market values.

    Warning:
        {experimental_feature}

    The IRR is the rate ``r`` that nullifies the Net Present Value:

    .. math::

        {formula}

    With:

    * :math:`T` the total number of days since the beginning
    * :math:`t_i` the number of days since the beginning for date :math:`i`
    * :math:`CF_i` the enhanced cashflow for date :math:`i`

      * CF of the first day is the opposite of the market value for this day: :math:`CF_0 = - MV_0`.
      * CF of the last day is increased by the market value for this day: :math:`CF_T = cash\_flow_T + MV_T`.
      * Otherwise CF is the input cash flow: :math:`CF_i = cash\_flow_i`.

    This equation is solved using the Newton's method.

    Args:
        cash_flows: The measure representing the cash flows.
        market_value: The measure representing the market value, used to enhanced the cashflows first and last value.
            If the cash flows don't need to be enhanced then ``0`` can be used.
        date: The date hierarchy. It must have a single date level.
        precision: The precision of the IRR value.

    See Also:
        The IRR `Wikipedia page <https://en.wikipedia.org/wiki/Internal_rate_of_return>`__.

    """
    if len(date) > 1:
        raise ValueError("The date hierarchy must have a single date level")
    return IrrMeasure(
        _cash_flows_measure=convert_to_measure_definition(cash_flows),
        _market_value_measure=convert_to_measure_definition(market_value),
        _date_hierarchy_identifier=date._identifier,
        _precision=precision,
    )
