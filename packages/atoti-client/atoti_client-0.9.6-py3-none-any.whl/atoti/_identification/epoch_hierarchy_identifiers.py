from .dimension_identifier import DimensionIdentifier
from .hierarchy_identifier import HierarchyIdentifier
from .level_name import LevelName

EPOCH_HIERARCHY_IDENTIFIER = HierarchyIdentifier(DimensionIdentifier("Epoch"), "Epoch")
BRANCH_LEVEL_NAME: LevelName = "Branch"
EPOCH_LEVEL_NAME: LevelName = "Epoch"
