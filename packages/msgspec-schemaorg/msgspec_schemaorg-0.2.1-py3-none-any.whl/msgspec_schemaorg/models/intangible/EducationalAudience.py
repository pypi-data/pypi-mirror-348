from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Audience import Audience
from typing import Optional, Union, Dict, List, Any


class EducationalAudience(Audience):
    """An EducationalAudience."""
    type: str = field(default_factory=lambda: "EducationalAudience", name="@type")
    educationalRole: Union[List[str], str, None] = None