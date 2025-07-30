from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Store import Store
from typing import Optional, Union, Dict, List, Any


class HobbyShop(Store):
    """A store that sells materials useful or necessary for various hobbies."""
    type: str = field(default_factory=lambda: "HobbyShop", name="@type")