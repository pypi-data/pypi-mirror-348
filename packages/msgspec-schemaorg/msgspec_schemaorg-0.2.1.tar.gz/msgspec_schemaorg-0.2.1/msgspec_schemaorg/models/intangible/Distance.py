from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Quantity import Quantity
from typing import Optional, Union, Dict, List, Any


class Distance(Quantity):
    """Properties that take Distances as values are of the form '&lt;Number&gt; &lt;Length unit of measure&gt;'. E.g., '7 ft'."""
    type: str = field(default_factory=lambda: "Distance", name="@type")