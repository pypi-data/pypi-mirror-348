from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalGuideline import MedicalGuideline
from typing import Optional, Union, Dict, List, Any


class MedicalGuidelineContraindication(MedicalGuideline):
    """A guideline contraindication that designates a process as harmful and where quality of the data supporting the contraindication is sound."""
    type: str = field(default_factory=lambda: "MedicalGuidelineContraindication", name="@type")