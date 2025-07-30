from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
    from msgspec_schemaorg.models.intangible.OccupationalExperienceRequirements import OccupationalExperienceRequirements
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class Occupation(Intangible):
    """A profession, may involve prolonged training and/or a formal qualification."""
    type: str = field(default_factory=lambda: "Occupation", name="@type")
    experienceRequirements: Union[List[Union[str, 'OccupationalExperienceRequirements']], Union[str, 'OccupationalExperienceRequirements'], None] = None
    responsibilities: Union[List[str], str, None] = None
    skills: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    occupationalCategory: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    qualifications: Union[List[Union[str, 'EducationalOccupationalCredential']], Union[str, 'EducationalOccupationalCredential'], None] = None
    occupationLocation: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None
    educationRequirements: Union[List[Union[str, 'EducationalOccupationalCredential']], Union[str, 'EducationalOccupationalCredential'], None] = None
    estimatedSalary: Union[List[Union[int | float, 'MonetaryAmount', 'MonetaryAmountDistribution']], Union[int | float, 'MonetaryAmount', 'MonetaryAmountDistribution'], None] = None