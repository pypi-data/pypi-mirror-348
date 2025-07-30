from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Store import Store
from typing import Optional, Union, Dict, List, Any


class PawnShop(Store):
    """A shop that will buy, or lend money against the security of, personal possessions."""
    type: str = field(default_factory=lambda: "PawnShop", name="@type")