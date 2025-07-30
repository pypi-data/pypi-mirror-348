from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class Cooperative(Organization):
    """An organization that is a joint project of multiple organizations or persons."""
    type: str = field(default_factory=lambda: "Cooperative", name="@type")