from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.DeliveryEvent import DeliveryEvent
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.Order import Order
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.product.Product import Product
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class ParcelDelivery(Intangible):
    """The delivery of a parcel either via the postal service or a commercial service."""
    type: str = field(default_factory=lambda: "ParcelDelivery", name="@type")
    expectedArrivalUntil: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    deliveryStatus: Union[List['DeliveryEvent'], 'DeliveryEvent', None] = None
    trackingNumber: Union[List[str], str, None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    carrier: Union[List['Organization'], 'Organization', None] = None
    hasDeliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None
    expectedArrivalFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    trackingUrl: Union[List['URL'], 'URL', None] = None
    partOfOrder: Union[List['Order'], 'Order', None] = None
    originAddress: Union[List['PostalAddress'], 'PostalAddress', None] = None
    deliveryAddress: Union[List['PostalAddress'], 'PostalAddress', None] = None
    itemShipped: Union[List['Product'], 'Product', None] = None