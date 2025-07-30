from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.SportsOrganization import SportsOrganization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.GenderType import GenderType
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class SportsTeam(SportsOrganization):
    """Organization: Sports team."""
    type: str = field(default_factory=lambda: "SportsTeam", name="@type")
    coach: Union[List['Person'], 'Person', None] = None
    gender: Union[List[Union[str, 'GenderType']], Union[str, 'GenderType'], None] = None
    athlete: Union[List['Person'], 'Person', None] = None