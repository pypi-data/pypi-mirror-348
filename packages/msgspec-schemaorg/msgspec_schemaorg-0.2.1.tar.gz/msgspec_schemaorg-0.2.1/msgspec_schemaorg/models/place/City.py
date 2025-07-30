from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class City(AdministrativeArea):
    """A city or town."""
    type: str = field(default_factory=lambda: "City", name="@type")