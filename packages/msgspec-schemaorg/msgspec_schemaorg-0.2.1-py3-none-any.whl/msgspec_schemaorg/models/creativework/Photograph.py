from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Photograph(CreativeWork):
    """A photograph."""
    type: str = field(default_factory=lambda: "Photograph", name="@type")