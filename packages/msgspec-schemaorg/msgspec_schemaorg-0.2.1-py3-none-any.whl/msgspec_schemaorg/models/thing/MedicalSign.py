from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalSignOrSymptom import MedicalSignOrSymptom
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.PhysicalExam import PhysicalExam
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import Optional, Union, Dict, List, Any


class MedicalSign(MedicalSignOrSymptom):
    """Any physical manifestation of a person's medical condition discoverable by objective diagnostic tests or physical examination."""
    type: str = field(default_factory=lambda: "MedicalSign", name="@type")
    identifyingTest: Union[List['MedicalTest'], 'MedicalTest', None] = None
    identifyingExam: Union[List['PhysicalExam'], 'PhysicalExam', None] = None