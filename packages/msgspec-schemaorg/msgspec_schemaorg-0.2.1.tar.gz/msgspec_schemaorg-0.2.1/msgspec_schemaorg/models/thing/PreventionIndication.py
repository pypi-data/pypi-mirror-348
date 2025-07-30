from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIndication import MedicalIndication
from typing import Optional, Union, Dict, List, Any


class PreventionIndication(MedicalIndication):
    """An indication for preventing an underlying condition, symptom, etc."""
    type: str = field(default_factory=lambda: "PreventionIndication", name="@type")