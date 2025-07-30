from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Thesis(CreativeWork):
    """A thesis or dissertation document submitted in support of candidature for an academic degree or professional qualification."""
    type: str = field(default_factory=lambda: "Thesis", name="@type")
    inSupportOf: Union[List[str], str, None] = None