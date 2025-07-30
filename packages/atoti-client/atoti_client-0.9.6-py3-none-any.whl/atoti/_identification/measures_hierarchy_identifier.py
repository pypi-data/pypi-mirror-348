from .dimension_identifier import DimensionIdentifier
from .hierarchy_identifier import HierarchyIdentifier

MEASURES_HIERARCHY_IDENTIFIER = HierarchyIdentifier(
    DimensionIdentifier("Measures"), "Measures"
)
