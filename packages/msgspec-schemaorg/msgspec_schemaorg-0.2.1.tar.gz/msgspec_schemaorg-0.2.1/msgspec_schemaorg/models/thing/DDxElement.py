from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIntangible import MedicalIntangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.MedicalSignOrSymptom import MedicalSignOrSymptom
from typing import Optional, Union, Dict, List, Any


class DDxElement(MedicalIntangible):
    """An alternative, closely-related condition typically considered later in the differential diagnosis process along with the signs that are used to distinguish it."""
    type: str = field(default_factory=lambda: "DDxElement", name="@type")
    diagnosis: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    distinguishingSign: Union[List['MedicalSignOrSymptom'], 'MedicalSignOrSymptom', None] = None