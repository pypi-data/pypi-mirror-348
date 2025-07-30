from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class SheetMusic(CreativeWork):
    """Printed music, as opposed to performed or recorded music."""
    type: str = field(default_factory=lambda: "SheetMusic", name="@type")