from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.UserInteraction import UserInteraction
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class UserComments(UserInteraction):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]]."""
    type: str = field(default_factory=lambda: "UserComments", name="@type")
    discusses: Union[List['CreativeWork'], 'CreativeWork', None] = None
    creator: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    commentTime: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    commentText: Union[List[str], str, None] = None
    replyToUrl: Union[List['URL'], 'URL', None] = None