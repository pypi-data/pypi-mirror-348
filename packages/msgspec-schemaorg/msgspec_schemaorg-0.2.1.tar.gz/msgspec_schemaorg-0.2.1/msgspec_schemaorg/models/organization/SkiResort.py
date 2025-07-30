from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Resort import Resort
from typing import Optional, Union, Dict, List, Any


class SkiResort(Resort):
    """A ski resort."""
    type: str = field(default_factory=lambda: "SkiResort", name="@type")