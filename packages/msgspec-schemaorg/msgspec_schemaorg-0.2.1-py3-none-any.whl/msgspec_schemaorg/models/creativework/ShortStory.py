from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class ShortStory(CreativeWork):
    """Short story or tale. A brief work of literature, usually written in narrative prose."""
    type: str = field(default_factory=lambda: "ShortStory", name="@type")