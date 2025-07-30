from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Permit(Intangible):
    """A permit issued by an organization, e.g. a parking pass."""
    type: str = field(default_factory=lambda: "Permit", name="@type")
    issuedBy: Union[List['Organization'], 'Organization', None] = None
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    issuedThrough: Union[List['Service'], 'Service', None] = None
    validUntil: Union[List[date], date, None] = None
    validFor: Union[List['Duration'], 'Duration', None] = None
    validIn: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None
    permitAudience: Union[List['Audience'], 'Audience', None] = None