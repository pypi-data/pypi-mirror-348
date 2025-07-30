from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class Audience(Intangible):
    """Intended audience for an item, i.e. the group for whom the item was created."""
    type: str = field(default_factory=lambda: "Audience", name="@type")
    geographicArea: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None
    audienceType: Union[List[str], str, None] = None