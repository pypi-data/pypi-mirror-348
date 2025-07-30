from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Store import Store
from typing import Optional, Union, Dict, List, Any


class ToyStore(Store):
    """A toy store."""
    type: str = field(default_factory=lambda: "ToyStore", name="@type")