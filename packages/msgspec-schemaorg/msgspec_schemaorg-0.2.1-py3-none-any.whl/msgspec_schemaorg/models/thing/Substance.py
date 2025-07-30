from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MaximumDoseSchedule import MaximumDoseSchedule
from typing import Optional, Union, Dict, List, Any


class Substance(MedicalEntity):
    """Any matter of defined composition that has discrete existence, whose origin may be biological, mineral or chemical."""
    type: str = field(default_factory=lambda: "Substance", name="@type")
    activeIngredient: Union[List[str], str, None] = None
    maximumIntake: Union[List['MaximumDoseSchedule'], 'MaximumDoseSchedule', None] = None