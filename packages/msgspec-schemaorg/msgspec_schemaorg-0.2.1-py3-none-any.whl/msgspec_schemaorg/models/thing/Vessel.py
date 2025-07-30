from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import Optional, Union, Dict, List, Any


class Vessel(AnatomicalStructure):
    """A component of the human body circulatory system comprised of an intricate network of hollow tubes that transport blood throughout the entire body."""
    type: str = field(default_factory=lambda: "Vessel", name="@type")