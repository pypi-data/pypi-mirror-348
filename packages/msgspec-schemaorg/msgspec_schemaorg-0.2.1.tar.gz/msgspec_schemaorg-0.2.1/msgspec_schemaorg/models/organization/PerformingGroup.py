from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class PerformingGroup(Organization):
    """A performance group, such as a band, an orchestra, or a circus."""
    type: str = field(default_factory=lambda: "PerformingGroup", name="@type")