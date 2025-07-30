from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MedicalEvidenceLevel import MedicalEvidenceLevel
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from datetime import date
from typing import Optional, Union, Dict, List, Any


class MedicalGuideline(MedicalEntity):
    """Any recommendation made by a standard society (e.g. ACC/AHA) or consensus statement that denotes how to diagnose and treat a particular condition. Note: this type should be used to tag the actual guideline recommendation; if the guideline recommendation occurs in a larger scholarly article, use MedicalScholarlyArticle to tag the overall article, not this type. Note also: the organization making the recommendation should be captured in the recognizingAuthority base property of MedicalEntity."""
    type: str = field(default_factory=lambda: "MedicalGuideline", name="@type")
    guidelineSubject: Union[List['MedicalEntity'], 'MedicalEntity', None] = None
    evidenceOrigin: Union[List[str], str, None] = None
    guidelineDate: Union[List[date], date, None] = None
    evidenceLevel: Union[List['MedicalEvidenceLevel'], 'MedicalEvidenceLevel', None] = None