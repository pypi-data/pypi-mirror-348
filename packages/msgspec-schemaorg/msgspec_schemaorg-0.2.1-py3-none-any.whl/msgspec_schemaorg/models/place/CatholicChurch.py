from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Church import Church
from typing import Optional, Union, Dict, List, Any


class CatholicChurch(Church):
    """A Catholic church."""
    type: str = field(default_factory=lambda: "CatholicChurch", name="@type")