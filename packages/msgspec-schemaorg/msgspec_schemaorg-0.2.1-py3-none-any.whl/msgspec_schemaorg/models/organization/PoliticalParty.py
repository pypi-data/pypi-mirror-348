from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class PoliticalParty(Organization):
    """Organization: Political Party."""
    type: str = field(default_factory=lambda: "PoliticalParty", name="@type")