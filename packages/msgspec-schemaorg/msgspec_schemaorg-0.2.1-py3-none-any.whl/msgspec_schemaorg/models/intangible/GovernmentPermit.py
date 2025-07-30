from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Permit import Permit
from typing import Optional, Union, Dict, List, Any


class GovernmentPermit(Permit):
    """A permit issued by a government agency."""
    type: str = field(default_factory=lambda: "GovernmentPermit", name="@type")