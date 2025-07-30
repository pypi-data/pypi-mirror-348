from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalSign import MedicalSign
from typing import Optional, Union, Dict, List, Any


class VitalSign(MedicalSign):
    """Vital signs are measures of various physiological functions in order to assess the most basic body functions."""
    type: str = field(default_factory=lambda: "VitalSign", name="@type")