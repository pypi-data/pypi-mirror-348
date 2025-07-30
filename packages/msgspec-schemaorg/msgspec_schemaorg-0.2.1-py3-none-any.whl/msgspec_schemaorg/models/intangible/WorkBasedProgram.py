from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.EducationalOccupationalProgram import EducationalOccupationalProgram
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
from typing import Optional, Union, Dict, List, Any


class WorkBasedProgram(EducationalOccupationalProgram):
    """A program with both an educational and employment component. Typically based at a workplace and structured around work-based learning, with the aim of instilling competencies related to an occupation. WorkBasedProgram is used to distinguish programs such as apprenticeships from school, college or other classroom based educational programs."""
    type: str = field(default_factory=lambda: "WorkBasedProgram", name="@type")
    occupationalCategory: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    trainingSalary: Union[List['MonetaryAmountDistribution'], 'MonetaryAmountDistribution', None] = None