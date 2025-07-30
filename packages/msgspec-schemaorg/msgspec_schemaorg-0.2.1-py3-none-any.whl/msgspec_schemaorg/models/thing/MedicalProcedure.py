from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.EventStatusType import EventStatusType
    from msgspec_schemaorg.enums.intangible.MedicalProcedureType import MedicalProcedureType
    from msgspec_schemaorg.enums.intangible.MedicalStudyStatus import MedicalStudyStatus
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class MedicalProcedure(MedicalEntity):
    """A process of care used in either a diagnostic, therapeutic, preventive or palliative capacity that relies on invasive (surgical), non-invasive, or other techniques."""
    type: str = field(default_factory=lambda: "MedicalProcedure", name="@type")
    status: Union[List[Union[str, 'MedicalStudyStatus', 'EventStatusType']], Union[str, 'MedicalStudyStatus', 'EventStatusType'], None] = None
    procedureType: Union[List['MedicalProcedureType'], 'MedicalProcedureType', None] = None
    preparation: Union[List[Union[str, 'MedicalEntity']], Union[str, 'MedicalEntity'], None] = None
    followup: Union[List[str], str, None] = None
    howPerformed: Union[List[str], str, None] = None
    bodyLocation: Union[List[str], str, None] = None