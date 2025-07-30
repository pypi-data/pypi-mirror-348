from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class DonateAction(TransferAction):
    """The act of providing goods, services, or money without compensation, often for philanthropic reasons."""
    type: str = field(default_factory=lambda: "DonateAction", name="@type")
    priceCurrency: Union[List[str], str, None] = None
    priceSpecification: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    price: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    recipient: Union[List[Union['Organization', 'Audience', 'ContactPoint', 'Person']], Union['Organization', 'Audience', 'ContactPoint', 'Person'], None] = None