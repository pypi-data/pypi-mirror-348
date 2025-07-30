from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.action.Action import Action
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.TextObject import TextObject
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
from typing import Optional, Union, Dict, List, Any


class Thing(SchemaOrgBase):
    """The most generic type of item."""
    type: str = field(default_factory=lambda: "Thing", name="@type")
    image: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    url: Union[List['URL'], 'URL', None] = None
    alternateName: Union[List[str], str, None] = None
    potentialAction: Union[List['Action'], 'Action', None] = None
    sameAs: Union[List['URL'], 'URL', None] = None
    identifier: Union[List[Union['URL', str, 'PropertyValue']], Union['URL', str, 'PropertyValue'], None] = None
    additionalType: Union[List[Union['URL', str]], Union['URL', str], None] = None
    subjectOf: Union[List[Union['CreativeWork', 'Event']], Union['CreativeWork', 'Event'], None] = None
    name: Union[List[str], str, None] = None
    description: Union[List[Union[str, 'TextObject']], Union[str, 'TextObject'], None] = None
    disambiguatingDescription: Union[List[str], str, None] = None
    mainEntityOfPage: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None