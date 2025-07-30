from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.ScholarlyArticle import ScholarlyArticle
from typing import Optional, Union, Dict, List, Any


class MedicalScholarlyArticle(ScholarlyArticle):
    """A scholarly article in the medical domain."""
    type: str = field(default_factory=lambda: "MedicalScholarlyArticle", name="@type")
    publicationType: Union[List[str], str, None] = None