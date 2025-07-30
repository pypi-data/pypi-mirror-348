from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from msgspec_schemaorg.utils import URL
from typing import Optional, Union, Dict, List, Any


class SportsOrganization(Organization):
    """Represents the collection of all sports organizations, including sports teams, governing bodies, and sports associations."""
    type: str = field(default_factory=lambda: "SportsOrganization", name="@type")
    sport: Union[List[Union['URL', str]], Union['URL', str], None] = None