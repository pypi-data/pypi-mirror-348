from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class ShoppingCenter(LocalBusiness):
    """A shopping center or mall."""
    type: str = field(default_factory=lambda: "ShoppingCenter", name="@type")