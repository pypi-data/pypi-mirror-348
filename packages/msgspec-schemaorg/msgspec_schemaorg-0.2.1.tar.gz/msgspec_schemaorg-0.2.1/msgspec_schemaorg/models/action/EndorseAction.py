from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ReactAction import ReactAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class EndorseAction(ReactAction):
    """An agent approves/certifies/likes/supports/sanctions an object."""
    type: str = field(default_factory=lambda: "EndorseAction", name="@type")
    endorsee: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None