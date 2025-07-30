from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.EntertainmentBusiness import EntertainmentBusiness
from typing import Optional, Union, Dict, List, Any


class ComedyClub(EntertainmentBusiness):
    """A comedy club."""
    type: str = field(default_factory=lambda: "ComedyClub", name="@type")