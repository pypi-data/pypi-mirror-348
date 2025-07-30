from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.EducationalOrganization import EducationalOrganization
from typing import Optional, Union, Dict, List, Any


class CollegeOrUniversity(EducationalOrganization):
    """A college, university, or other third-level educational institution."""
    type: str = field(default_factory=lambda: "CollegeOrUniversity", name="@type")