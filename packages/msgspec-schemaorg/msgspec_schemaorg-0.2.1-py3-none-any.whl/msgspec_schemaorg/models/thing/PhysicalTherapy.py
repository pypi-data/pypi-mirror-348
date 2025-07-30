from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class PhysicalTherapy(MedicalTherapy):
    """A process of progressive physical care and rehabilitation aimed at improving a health condition."""
    type: str = field(default_factory=lambda: "PhysicalTherapy", name="@type")