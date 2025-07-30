from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class Quantity(Intangible):
    """Quantities such as distance, time, mass, weight, etc. Particular instances of say Mass are entities like '3 kg' or '4 milligrams'."""
    type: str = field(default_factory=lambda: "Quantity", name="@type")