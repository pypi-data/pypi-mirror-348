from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BroadcastService import BroadcastService
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class PublicationEvent(Event):
    """A PublicationEvent corresponds indifferently to the event of publication for a CreativeWork of any type, e.g. a broadcast event, an on-demand event, a book/journal publication via a variety of delivery media."""
    type: str = field(default_factory=lambda: "PublicationEvent", name="@type")
    free: Union[List[bool], bool, None] = None
    publishedOn: Union[List['BroadcastService'], 'BroadcastService', None] = None
    publishedBy: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None