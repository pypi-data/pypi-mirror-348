from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PeopleAudience import PeopleAudience
from typing import Optional, Union, Dict, List, Any


class ParentAudience(PeopleAudience):
    """A set of characteristics describing parents, who can be interested in viewing some content."""
    type: str = field(default_factory=lambda: "ParentAudience", name="@type")
    childMaxAge: Union[List[int | float], int | float, None] = None
    childMinAge: Union[List[int | float], int | float, None] = None