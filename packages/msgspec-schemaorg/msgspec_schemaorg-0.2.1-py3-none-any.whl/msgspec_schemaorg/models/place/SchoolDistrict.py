from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class SchoolDistrict(AdministrativeArea):
    """A School District is an administrative area for the administration of schools."""
    type: str = field(default_factory=lambda: "SchoolDistrict", name="@type")