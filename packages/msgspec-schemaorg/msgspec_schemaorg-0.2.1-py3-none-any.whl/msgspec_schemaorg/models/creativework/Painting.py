from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Painting(CreativeWork):
    """A painting."""
    type: str = field(default_factory=lambda: "Painting", name="@type")