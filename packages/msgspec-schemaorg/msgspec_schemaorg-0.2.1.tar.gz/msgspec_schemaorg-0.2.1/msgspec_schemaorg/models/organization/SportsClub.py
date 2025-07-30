from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.SportsActivityLocation import SportsActivityLocation
from typing import Optional, Union, Dict, List, Any


class SportsClub(SportsActivityLocation):
    """A sports club."""
    type: str = field(default_factory=lambda: "SportsClub", name="@type")