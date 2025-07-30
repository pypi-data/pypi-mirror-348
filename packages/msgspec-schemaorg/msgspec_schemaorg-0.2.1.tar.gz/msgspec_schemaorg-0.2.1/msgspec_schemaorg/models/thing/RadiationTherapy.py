from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class RadiationTherapy(MedicalTherapy):
    """A process of care using radiation aimed at improving a health condition."""
    type: str = field(default_factory=lambda: "RadiationTherapy", name="@type")