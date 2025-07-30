from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Message(CreativeWork):
    """A single message from a sender to one or more organizations or people."""
    type: str = field(default_factory=lambda: "Message", name="@type")
    dateReceived: Union[List[datetime], datetime, None] = None
    toRecipient: Union[List[Union['Audience', 'Organization', 'ContactPoint', 'Person']], Union['Audience', 'Organization', 'ContactPoint', 'Person'], None] = None
    sender: Union[List[Union['Person', 'Audience', 'Organization']], Union['Person', 'Audience', 'Organization'], None] = None
    bccRecipient: Union[List[Union['Organization', 'ContactPoint', 'Person']], Union['Organization', 'ContactPoint', 'Person'], None] = None
    ccRecipient: Union[List[Union['Organization', 'ContactPoint', 'Person']], Union['Organization', 'ContactPoint', 'Person'], None] = None
    dateSent: Union[List[datetime], datetime, None] = None
    dateRead: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    recipient: Union[List[Union['Organization', 'Audience', 'ContactPoint', 'Person']], Union['Organization', 'Audience', 'ContactPoint', 'Person'], None] = None
    messageAttachment: Union[List['CreativeWork'], 'CreativeWork', None] = None