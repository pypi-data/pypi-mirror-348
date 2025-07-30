from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPage import WebPage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MedicalAudience import MedicalAudience
    from msgspec_schemaorg.enums.intangible.MedicalAudienceType import MedicalAudienceType
from typing import Optional, Union, Dict, List, Any


class MedicalWebPage(WebPage):
    """A web page that provides medical information."""
    type: str = field(default_factory=lambda: "MedicalWebPage", name="@type")
    medicalAudience: Union[List[Union['MedicalAudienceType', 'MedicalAudience']], Union['MedicalAudienceType', 'MedicalAudience'], None] = None
    aspect: Union[List[str], str, None] = None