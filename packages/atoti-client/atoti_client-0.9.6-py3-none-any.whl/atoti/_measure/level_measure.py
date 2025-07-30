from dataclasses import KW_ONLY, dataclass
from typing import final

from typing_extensions import override

from .._identification import LevelIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_definition import MeasureDefinition


@final
@dataclass(eq=False, frozen=True)
class LevelMeasure(MeasureDefinition):
    _level_identifier: LevelIdentifier
    _: KW_ONLY

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        return java_api.create_measure(
            identifier,
            "LEVEL",
            self._level_identifier._java_description,
            cube_name=cube_name,
        )
