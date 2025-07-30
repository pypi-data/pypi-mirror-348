from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class GovernmentService(Service):
    """A service provided by a government organization, e.g. food stamps, veterans benefits, etc."""
    type: str = field(default_factory=lambda: "GovernmentService", name="@type")
    jurisdiction: Union[List[Union[str, 'AdministrativeArea']], Union[str, 'AdministrativeArea'], None] = None
    serviceOperator: Union[List['Organization'], 'Organization', None] = None