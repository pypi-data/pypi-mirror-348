from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.DigitalDocument import DigitalDocument
from typing import Optional, Union, Dict, List, Any


class NoteDigitalDocument(DigitalDocument):
    """A file containing a note, primarily for the author."""
    type: str = field(default_factory=lambda: "NoteDigitalDocument", name="@type")