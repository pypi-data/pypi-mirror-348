from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class MedicalSignOrSymptom(MedicalCondition):
    """Any feature associated or not with a medical condition. In medicine a symptom is generally subjective while a sign is objective."""
    type: str = field(default_factory=lambda: "MedicalSignOrSymptom", name="@type")
    possibleTreatment: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None