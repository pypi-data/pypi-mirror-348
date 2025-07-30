from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import Optional, Union, Dict, List, Any


class Ligament(AnatomicalStructure):
    """A short band of tough, flexible, fibrous connective tissue that functions to connect multiple bones, cartilages, and structurally support joints."""
    type: str = field(default_factory=lambda: "Ligament", name="@type")