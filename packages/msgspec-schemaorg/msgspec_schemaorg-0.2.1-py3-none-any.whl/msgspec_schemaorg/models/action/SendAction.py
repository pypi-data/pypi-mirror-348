from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class SendAction(TransferAction):
    """The act of physically/electronically dispatching an object for transfer from an origin to a destination. Related actions:\\n\\n* [[ReceiveAction]]: The reciprocal of SendAction.\\n* [[GiveAction]]: Unlike GiveAction, SendAction does not imply the transfer of ownership (e.g. I can send you my laptop, but I'm not necessarily giving it to you)."""
    type: str = field(default_factory=lambda: "SendAction", name="@type")
    recipient: Union[List[Union['Organization', 'Audience', 'ContactPoint', 'Person']], Union['Organization', 'Audience', 'ContactPoint', 'Person'], None] = None
    deliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None