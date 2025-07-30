from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class ReceiveAction(TransferAction):
    """The act of physically/electronically taking delivery of an object that has been transferred from an origin to a destination. Reciprocal of SendAction.\\n\\nRelated actions:\\n\\n* [[SendAction]]: The reciprocal of ReceiveAction.\\n* [[TakeAction]]: Unlike TakeAction, ReceiveAction does not imply that the ownership has been transferred (e.g. I can receive a package, but it does not mean the package is now mine)."""
    type: str = field(default_factory=lambda: "ReceiveAction", name="@type")
    sender: Union[List[Union['Person', 'Audience', 'Organization']], Union['Person', 'Audience', 'Organization'], None] = None
    deliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None