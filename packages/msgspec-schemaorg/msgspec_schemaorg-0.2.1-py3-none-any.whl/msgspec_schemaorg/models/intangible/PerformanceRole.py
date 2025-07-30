from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Role import Role
from typing import Optional, Union, Dict, List, Any


class PerformanceRole(Role):
    """A PerformanceRole is a Role that some entity places with regard to a theatrical performance, e.g. in a Movie, TVSeries etc."""
    type: str = field(default_factory=lambda: "PerformanceRole", name="@type")
    characterName: Union[List[str], str, None] = None