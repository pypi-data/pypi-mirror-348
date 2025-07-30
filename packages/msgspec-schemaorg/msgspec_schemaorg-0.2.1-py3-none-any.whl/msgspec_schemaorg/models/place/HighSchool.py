from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.EducationalOrganization import EducationalOrganization
from typing import Optional, Union, Dict, List, Any


class HighSchool(EducationalOrganization):
    """A high school."""
    type: str = field(default_factory=lambda: "HighSchool", name="@type")