from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class GiveAction(TransferAction):
    """The act of transferring ownership of an object to a destination. Reciprocal of TakeAction.\\n\\nRelated actions:\\n\\n* [[TakeAction]]: Reciprocal of GiveAction.\\n* [[SendAction]]: Unlike SendAction, GiveAction implies that ownership is being transferred (e.g. I may send my laptop to you, but that doesn't mean I'm giving it to you)."""
    type: str = field(default_factory=lambda: "GiveAction", name="@type")
    recipient: Union[List[Union['Organization', 'Audience', 'ContactPoint', 'Person']], Union['Organization', 'Audience', 'ContactPoint', 'Person'], None] = None