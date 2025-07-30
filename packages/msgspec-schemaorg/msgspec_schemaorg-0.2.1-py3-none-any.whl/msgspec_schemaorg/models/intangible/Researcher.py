from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Audience import Audience
from typing import Optional, Union, Dict, List, Any


class Researcher(Audience):
    """Researchers."""
    type: str = field(default_factory=lambda: "Researcher", name="@type")