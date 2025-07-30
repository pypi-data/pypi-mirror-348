from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Role import Role
from typing import Optional, Union, Dict, List, Any


class OrganizationRole(Role):
    """A subclass of Role used to describe roles within organizations."""
    type: str = field(default_factory=lambda: "OrganizationRole", name="@type")
    numberedPosition: Union[List[int | float], int | float, None] = None