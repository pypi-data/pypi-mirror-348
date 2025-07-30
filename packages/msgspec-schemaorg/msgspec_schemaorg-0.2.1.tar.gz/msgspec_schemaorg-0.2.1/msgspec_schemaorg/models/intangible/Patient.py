from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.MedicalAudience import MedicalAudience
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.product.Drug import Drug
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
from typing import Optional, Union, Dict, List, Any


class Patient(MedicalAudience):
    """A patient is any person recipient of health care services."""
    type: str = field(default_factory=lambda: "Patient", name="@type")
    diagnosis: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    healthCondition: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    drug: Union[List['Drug'], 'Drug', None] = None