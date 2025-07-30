from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.DigitalDocument import DigitalDocument
from typing import Optional, Union, Dict, List, Any


class TextDigitalDocument(DigitalDocument):
    """A file composed primarily of text."""
    type: str = field(default_factory=lambda: "TextDigitalDocument", name="@type")