from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Store import Store
from typing import Optional, Union, Dict, List, Any


class HomeGoodsStore(Store):
    """A home goods store."""
    type: str = field(default_factory=lambda: "HomeGoodsStore", name="@type")