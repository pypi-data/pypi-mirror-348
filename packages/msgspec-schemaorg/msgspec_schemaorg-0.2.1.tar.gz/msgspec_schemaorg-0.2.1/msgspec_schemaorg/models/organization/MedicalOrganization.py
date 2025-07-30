from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MedicalSpecialty import MedicalSpecialty
from typing import Optional, Union, Dict, List, Any


class MedicalOrganization(Organization):
    """A medical organization (physical or not), such as hospital, institution or clinic."""
    type: str = field(default_factory=lambda: "MedicalOrganization", name="@type")
    healthPlanNetworkId: Union[List[str], str, None] = None
    isAcceptingNewPatients: Union[List[bool], bool, None] = None
    medicalSpecialty: Union[List['MedicalSpecialty'], 'MedicalSpecialty', None] = None