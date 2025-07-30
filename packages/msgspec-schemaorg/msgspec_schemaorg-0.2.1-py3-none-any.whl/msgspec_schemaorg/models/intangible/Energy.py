from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Quantity import Quantity
from typing import Optional, Union, Dict, List, Any


class Energy(Quantity):
    """Properties that take Energy as values are of the form '&lt;Number&gt; &lt;Energy unit of measure&gt;'."""
    type: str = field(default_factory=lambda: "Energy", name="@type")