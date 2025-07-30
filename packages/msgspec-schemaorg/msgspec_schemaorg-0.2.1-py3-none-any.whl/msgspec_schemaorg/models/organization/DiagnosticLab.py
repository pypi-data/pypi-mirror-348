from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import Optional, Union, Dict, List, Any


class DiagnosticLab(MedicalOrganization):
    """A medical laboratory that offers on-site or off-site diagnostic services."""
    type: str = field(default_factory=lambda: "DiagnosticLab", name="@type")
    availableTest: Union[List['MedicalTest'], 'MedicalTest', None] = None