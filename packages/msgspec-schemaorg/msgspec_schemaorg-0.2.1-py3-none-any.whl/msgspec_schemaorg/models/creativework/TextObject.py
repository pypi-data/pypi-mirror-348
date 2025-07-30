from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class TextObject(MediaObject):
    """A text file. The text can be unformatted or contain markup, html, etc."""
    type: str = field(default_factory=lambda: "TextObject", name="@type")