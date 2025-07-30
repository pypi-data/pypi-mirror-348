from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalBusiness import MedicalBusiness
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.enums.intangible.MedicalSpecialty import MedicalSpecialty
    from msgspec_schemaorg.models.organization.Hospital import Hospital
    from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class Physician(MedicalBusiness):
    """An individual physician or a physician's office considered as a [[MedicalOrganization]]."""
    type: str = field(default_factory=lambda: "Physician", name="@type")
    usNPI: Union[List[str], str, None] = None
    occupationalCategory: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    medicalSpecialty: Union[List['MedicalSpecialty'], 'MedicalSpecialty', None] = None
    hospitalAffiliation: Union[List['Hospital'], 'Hospital', None] = None
    availableService: Union[List[Union['MedicalProcedure', 'MedicalTest', 'MedicalTherapy']], Union['MedicalProcedure', 'MedicalTest', 'MedicalTherapy'], None] = None