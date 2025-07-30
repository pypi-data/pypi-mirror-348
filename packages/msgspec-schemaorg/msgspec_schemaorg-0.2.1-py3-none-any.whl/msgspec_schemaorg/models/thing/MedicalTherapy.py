from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.TherapeuticProcedure import TherapeuticProcedure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalContraindication import MedicalContraindication
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class MedicalTherapy(TherapeuticProcedure):
    """Any medical intervention designed to prevent, treat, and cure human diseases and medical conditions, including both curative and palliative therapies. Medical therapies are typically processes of care relying upon pharmacotherapy, behavioral therapy, supportive therapy (with fluid or nutrition for example), or detoxification (e.g. hemodialysis) aimed at improving or preventing a health condition."""
    type: str = field(default_factory=lambda: "MedicalTherapy", name="@type")
    contraindication: Union[List[Union[str, 'MedicalContraindication']], Union[str, 'MedicalContraindication'], None] = None
    seriousAdverseOutcome: Union[List['MedicalEntity'], 'MedicalEntity', None] = None
    duplicateTherapy: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None