from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PeopleAudience import PeopleAudience
from typing import Optional, Union, Dict, List, Any


class MedicalAudience(PeopleAudience):
    """Target audiences for medical web pages."""
    type: str = field(default_factory=lambda: "MedicalAudience", name="@type")