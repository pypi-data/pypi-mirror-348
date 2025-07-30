from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalGuideline import MedicalGuideline
from typing import Optional, Union, Dict, List, Any


class MedicalGuidelineRecommendation(MedicalGuideline):
    """A guideline recommendation that is regarded as efficacious and where quality of the data supporting the recommendation is sound."""
    type: str = field(default_factory=lambda: "MedicalGuidelineRecommendation", name="@type")
    recommendationStrength: Union[List[str], str, None] = None