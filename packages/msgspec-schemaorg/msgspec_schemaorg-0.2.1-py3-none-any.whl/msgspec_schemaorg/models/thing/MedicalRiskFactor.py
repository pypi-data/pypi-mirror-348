from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class MedicalRiskFactor(MedicalEntity):
    """A risk factor is anything that increases a person's likelihood of developing or contracting a disease, medical condition, or complication."""
    type: str = field(default_factory=lambda: "MedicalRiskFactor", name="@type")
    increasesRiskOf: Union[List['MedicalEntity'], 'MedicalEntity', None] = None