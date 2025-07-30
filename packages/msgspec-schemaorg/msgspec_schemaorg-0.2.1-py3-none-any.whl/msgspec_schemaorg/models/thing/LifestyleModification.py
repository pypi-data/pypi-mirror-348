from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class LifestyleModification(MedicalEntity):
    """A process of care involving exercise, changes to diet, fitness routines, and other lifestyle changes aimed at improving a health condition."""
    type: str = field(default_factory=lambda: "LifestyleModification", name="@type")