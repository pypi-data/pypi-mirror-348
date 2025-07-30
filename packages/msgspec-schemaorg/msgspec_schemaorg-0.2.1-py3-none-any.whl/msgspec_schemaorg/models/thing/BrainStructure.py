from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import Optional, Union, Dict, List, Any


class BrainStructure(AnatomicalStructure):
    """Any anatomical structure which pertains to the soft nervous tissue functioning as the coordinating center of sensation and intellectual and nervous activity."""
    type: str = field(default_factory=lambda: "BrainStructure", name="@type")