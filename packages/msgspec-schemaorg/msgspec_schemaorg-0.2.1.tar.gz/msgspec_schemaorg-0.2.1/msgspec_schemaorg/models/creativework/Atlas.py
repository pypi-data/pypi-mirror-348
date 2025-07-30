from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Atlas(CreativeWork):
    """A collection or bound volume of maps, charts, plates or tables, physical or in media form illustrating any subject."""
    type: str = field(default_factory=lambda: "Atlas", name="@type")