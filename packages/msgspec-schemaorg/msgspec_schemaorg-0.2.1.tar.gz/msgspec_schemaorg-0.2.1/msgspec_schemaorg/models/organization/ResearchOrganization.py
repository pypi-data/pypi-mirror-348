from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class ResearchOrganization(Organization):
    """A Research Organization (e.g. scientific institute, research company)."""
    type: str = field(default_factory=lambda: "ResearchOrganization", name="@type")