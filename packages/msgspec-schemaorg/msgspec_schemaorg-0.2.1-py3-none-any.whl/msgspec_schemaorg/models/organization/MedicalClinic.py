from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MedicalSpecialty import MedicalSpecialty
    from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class MedicalClinic(MedicalOrganization):
    """A facility, often associated with a hospital or medical school, that is devoted to the specific diagnosis and/or healthcare. Previously limited to outpatients but with evolution it may be open to inpatients as well."""
    type: str = field(default_factory=lambda: "MedicalClinic", name="@type")
    medicalSpecialty: Union[List['MedicalSpecialty'], 'MedicalSpecialty', None] = None
    availableService: Union[List[Union['MedicalProcedure', 'MedicalTest', 'MedicalTherapy']], Union['MedicalProcedure', 'MedicalTest', 'MedicalTherapy'], None] = None