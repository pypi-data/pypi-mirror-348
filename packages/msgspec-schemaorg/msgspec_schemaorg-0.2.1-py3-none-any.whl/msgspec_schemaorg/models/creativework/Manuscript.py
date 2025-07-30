from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Manuscript(CreativeWork):
    """A book, document, or piece of music written by hand rather than typed or printed."""
    type: str = field(default_factory=lambda: "Manuscript", name="@type")