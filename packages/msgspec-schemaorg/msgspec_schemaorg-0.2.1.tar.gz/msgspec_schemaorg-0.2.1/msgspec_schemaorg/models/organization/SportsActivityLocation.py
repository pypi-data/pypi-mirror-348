from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class SportsActivityLocation(LocalBusiness):
    """A sports location, such as a playing field."""
    type: str = field(default_factory=lambda: "SportsActivityLocation", name="@type")