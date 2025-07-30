from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.EducationalOrganization import EducationalOrganization
from typing import Optional, Union, Dict, List, Any


class ElementarySchool(EducationalOrganization):
    """An elementary school."""
    type: str = field(default_factory=lambda: "ElementarySchool", name="@type")