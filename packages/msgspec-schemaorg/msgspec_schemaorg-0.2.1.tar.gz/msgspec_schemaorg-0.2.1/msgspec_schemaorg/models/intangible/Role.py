from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Role(Intangible):
    """Represents additional information about a relationship or property. For example a Role can be used to say that a 'member' role linking some SportsTeam to a player occurred during a particular time period. Or that a Person's 'actor' role in a Movie was for some particular characterName. Such properties can be attached to a Role entity, which is then associated with the main entities using ordinary properties like 'member' or 'actor'.\\n\\nSee also [blog post](http://blog.schema.org/2014/06/introducing-role.html)."""
    type: str = field(default_factory=lambda: "Role", name="@type")
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    roleName: Union[List[Union['URL', str]], Union['URL', str], None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    namedPosition: Union[List[Union['URL', str]], Union['URL', str], None] = None