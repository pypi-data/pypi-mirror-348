from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.organization.ArchiveOrganization import ArchiveOrganization
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class ArchiveComponent(CreativeWork):
    """{'@language': 'en', '@value': 'An intangible type to be applied to any archive content, carrying with it a set of properties required to describe archival items and collections.'}"""
    type: str = field(default_factory=lambda: "ArchiveComponent", name="@type")
    itemLocation: Union[List[Union[str, 'PostalAddress', 'Place']], Union[str, 'PostalAddress', 'Place'], None] = None
    holdingArchive: Union[List['ArchiveOrganization'], 'ArchiveOrganization', None] = None