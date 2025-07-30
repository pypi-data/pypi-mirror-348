from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class GovernmentOrganization(Organization):
    """A governmental organization or agency."""
    type: str = field(default_factory=lambda: "GovernmentOrganization", name="@type")