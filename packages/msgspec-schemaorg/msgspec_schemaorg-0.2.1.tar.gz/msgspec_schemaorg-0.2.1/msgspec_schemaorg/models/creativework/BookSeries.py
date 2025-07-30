from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWorkSeries import CreativeWorkSeries
from typing import Optional, Union, Dict, List, Any


class BookSeries(CreativeWorkSeries):
    """A series of books. Included books can be indicated with the hasPart property."""
    type: str = field(default_factory=lambda: "BookSeries", name="@type")