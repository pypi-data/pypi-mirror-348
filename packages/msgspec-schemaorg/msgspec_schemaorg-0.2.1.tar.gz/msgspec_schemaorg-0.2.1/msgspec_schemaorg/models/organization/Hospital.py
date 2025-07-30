from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.EmergencyService import EmergencyService
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Dataset import Dataset
    from msgspec_schemaorg.models.intangible.CDCPMDRecord import CDCPMDRecord
    from msgspec_schemaorg.enums.intangible.MedicalSpecialty import MedicalSpecialty
    from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class Hospital(EmergencyService):
    """A hospital."""
    type: str = field(default_factory=lambda: "Hospital", name="@type")
    healthcareReportingData: Union[List[Union['CDCPMDRecord', 'Dataset']], Union['CDCPMDRecord', 'Dataset'], None] = None
    medicalSpecialty: Union[List['MedicalSpecialty'], 'MedicalSpecialty', None] = None
    availableService: Union[List[Union['MedicalProcedure', 'MedicalTest', 'MedicalTherapy']], Union['MedicalProcedure', 'MedicalTest', 'MedicalTherapy'], None] = None