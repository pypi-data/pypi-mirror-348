from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class SearchRescueOrganization(Organization):
    """A Search and Rescue organization of some kind."""
    type: str = field(default_factory=lambda: "SearchRescueOrganization", name="@type")