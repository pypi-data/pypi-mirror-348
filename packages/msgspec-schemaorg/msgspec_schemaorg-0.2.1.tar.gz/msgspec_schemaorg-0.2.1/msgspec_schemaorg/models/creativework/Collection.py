from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Collection(CreativeWork):
    """A collection of items, e.g. creative works or products."""
    type: str = field(default_factory=lambda: "Collection", name="@type")
    collectionSize: Union[List[int], int, None] = None