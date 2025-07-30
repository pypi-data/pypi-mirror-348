from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Drawing(CreativeWork):
    """A picture or diagram made with a pencil, pen, or crayon rather than paint."""
    type: str = field(default_factory=lambda: "Drawing", name="@type")