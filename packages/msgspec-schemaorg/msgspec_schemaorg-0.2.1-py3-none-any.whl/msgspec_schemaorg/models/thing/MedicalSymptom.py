from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalSignOrSymptom import MedicalSignOrSymptom
from typing import Optional, Union, Dict, List, Any


class MedicalSymptom(MedicalSignOrSymptom):
    """Any complaint sensed and expressed by the patient (therefore defined as subjective)  like stomachache, lower-back pain, or fatigue."""
    type: str = field(default_factory=lambda: "MedicalSymptom", name="@type")