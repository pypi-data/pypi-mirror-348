from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class Specialty(Enumeration):
    """Any branch of a field in which people typically develop specific expertise, usually after significant study, time, and effort."""
    type: str = field(default_factory=lambda: "Specialty", name="@type")