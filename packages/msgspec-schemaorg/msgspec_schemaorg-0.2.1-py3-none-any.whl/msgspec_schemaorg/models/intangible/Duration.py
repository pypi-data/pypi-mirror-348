from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Quantity import Quantity
from typing import Optional, Union, Dict, List, Any


class Duration(Quantity):
    """Quantity: Duration (use [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601))."""
    type: str = field(default_factory=lambda: "Duration", name="@type")