from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Physician import Physician
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import Optional, Union, Dict, List, Any


class IndividualPhysician(Physician):
    """An individual medical practitioner. For their official address use [[address]], for affiliations to hospitals use [[hospitalAffiliation]]. 
The [[practicesAt]] property can be used to indicate [[MedicalOrganization]] hospitals, clinics, pharmacies etc. where this physician practices."""
    type: str = field(default_factory=lambda: "IndividualPhysician", name="@type")
    practicesAt: Union[List['MedicalOrganization'], 'MedicalOrganization', None] = None