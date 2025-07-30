from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class OccupationalExperienceRequirements(Intangible):
    """Indicates employment-related experience requirements, e.g. [[monthsOfExperience]]."""
    type: str = field(default_factory=lambda: "OccupationalExperienceRequirements", name="@type")
    monthsOfExperience: Union[List[int | float], int | float, None] = None