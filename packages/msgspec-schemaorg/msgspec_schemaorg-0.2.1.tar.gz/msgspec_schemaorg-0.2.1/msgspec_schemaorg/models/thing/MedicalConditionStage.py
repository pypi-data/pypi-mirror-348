from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIntangible import MedicalIntangible
from typing import Optional, Union, Dict, List, Any


class MedicalConditionStage(MedicalIntangible):
    """A stage of a medical condition, such as 'Stage IIIa'."""
    type: str = field(default_factory=lambda: "MedicalConditionStage", name="@type")
    subStageSuffix: Union[List[str], str, None] = None
    stageAsNumber: Union[List[int | float], int | float, None] = None