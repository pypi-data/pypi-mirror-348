from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AllocateAction import AllocateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class AuthorizeAction(AllocateAction):
    """The act of granting permission to an object."""
    type: str = field(default_factory=lambda: "AuthorizeAction", name="@type")
    recipient: Union[List[Union['Organization', 'Audience', 'ContactPoint', 'Person']], Union['Organization', 'Audience', 'ContactPoint', 'Person'], None] = None