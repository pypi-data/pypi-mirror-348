from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.DigitalDocument import DigitalDocument
from typing import Optional, Union, Dict, List, Any


class PresentationDigitalDocument(DigitalDocument):
    """A file containing slides or used for a presentation."""
    type: str = field(default_factory=lambda: "PresentationDigitalDocument", name="@type")