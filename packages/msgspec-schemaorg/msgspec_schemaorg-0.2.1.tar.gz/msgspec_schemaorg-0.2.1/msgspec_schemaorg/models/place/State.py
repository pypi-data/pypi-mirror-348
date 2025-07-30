from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class State(AdministrativeArea):
    """A state or province of a country."""
    type: str = field(default_factory=lambda: "State", name="@type")