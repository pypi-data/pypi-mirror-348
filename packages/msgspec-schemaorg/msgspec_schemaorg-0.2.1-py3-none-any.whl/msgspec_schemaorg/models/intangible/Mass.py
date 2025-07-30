from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Quantity import Quantity
from typing import Optional, Union, Dict, List, Any


class Mass(Quantity):
    """Properties that take Mass as values are of the form '&lt;Number&gt; &lt;Mass unit of measure&gt;'. E.g., '7 kg'."""
    type: str = field(default_factory=lambda: "Mass", name="@type")