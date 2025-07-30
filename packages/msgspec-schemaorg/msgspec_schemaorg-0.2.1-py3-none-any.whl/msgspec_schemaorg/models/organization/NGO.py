from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class NGO(Organization):
    """Organization: Non-governmental Organization."""
    type: str = field(default_factory=lambda: "NGO", name="@type")