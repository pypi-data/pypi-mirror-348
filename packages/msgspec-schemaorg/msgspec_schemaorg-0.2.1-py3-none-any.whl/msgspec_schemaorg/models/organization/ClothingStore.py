from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Store import Store
from typing import Optional, Union, Dict, List, Any


class ClothingStore(Store):
    """A clothing store."""
    type: str = field(default_factory=lambda: "ClothingStore", name="@type")