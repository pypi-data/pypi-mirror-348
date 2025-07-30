from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class StructuredValue(Intangible):
    """Structured values are used when the value of a property has a more complex structure than simply being a textual value or a reference to another thing."""
    type: str = field(default_factory=lambda: "StructuredValue", name="@type")