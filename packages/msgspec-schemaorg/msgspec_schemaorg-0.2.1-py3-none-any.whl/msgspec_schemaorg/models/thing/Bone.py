from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import Optional, Union, Dict, List, Any


class Bone(AnatomicalStructure):
    """Rigid connective tissue that comprises up the skeletal structure of the human body."""
    type: str = field(default_factory=lambda: "Bone", name="@type")