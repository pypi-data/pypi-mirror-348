from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.EducationalOrganization import EducationalOrganization
from typing import Optional, Union, Dict, List, Any


class School(EducationalOrganization):
    """A school."""
    type: str = field(default_factory=lambda: "School", name="@type")