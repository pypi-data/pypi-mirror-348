from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.AggregateOffer import AggregateOffer
    from msgspec_schemaorg.models.intangible.BusinessEntityType import BusinessEntityType
    from msgspec_schemaorg.models.intangible.BusinessFunction import BusinessFunction
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.enums.intangible.ItemAvailability import ItemAvailability
    from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
    from msgspec_schemaorg.models.intangible.MenuItem import MenuItem
    from msgspec_schemaorg.enums.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.intangible.Trip import Trip
    from msgspec_schemaorg.models.intangible.TypeAndQuantityNode import TypeAndQuantityNode
    from msgspec_schemaorg.models.intangible.WarrantyPromise import WarrantyPromise
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class Demand(Intangible):
    """A demand entity represents the public, not necessarily binding, not necessarily exclusive, announcement by an organization or person to seek a certain type of goods or services. For describing demand using this type, the very same properties used for Offer apply."""
    type: str = field(default_factory=lambda: "Demand", name="@type")
    warranty: Union[List['WarrantyPromise'], 'WarrantyPromise', None] = None
    gtin8: Union[List[str], str, None] = None
    asin: Union[List[Union['URL', str]], Union['URL', str], None] = None
    eligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    eligibleTransactionVolume: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    availability: Union[List['ItemAvailability'], 'ItemAvailability', None] = None
    businessFunction: Union[List['BusinessFunction'], 'BusinessFunction', None] = None
    inventoryLevel: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    advanceBookingRequirement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    eligibleDuration: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    availableAtOrFrom: Union[List['Place'], 'Place', None] = None
    seller: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    itemOffered: Union[List[Union['Service', 'AggregateOffer', 'CreativeWork', 'Event', 'MenuItem', 'Product', 'Trip']], Union['Service', 'AggregateOffer', 'CreativeWork', 'Event', 'MenuItem', 'Product', 'Trip'], None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    mpn: Union[List[str], str, None] = None
    gtin12: Union[List[str], str, None] = None
    ineligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    eligibleQuantity: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    gtin13: Union[List[str], str, None] = None
    availabilityStarts: Union[List[Union[datetime, date, time]], Union[datetime, date, time], None] = None
    eligibleCustomerType: Union[List['BusinessEntityType'], 'BusinessEntityType', None] = None
    gtin: Union[List[Union['URL', str]], Union['URL', str], None] = None
    availabilityEnds: Union[List[Union[datetime, date, time]], Union[datetime, date, time], None] = None
    priceSpecification: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    sku: Union[List[str], str, None] = None
    gtin14: Union[List[str], str, None] = None
    serialNumber: Union[List[str], str, None] = None
    availableDeliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None
    acceptedPaymentMethod: Union[List[Union[str, 'LoanOrCredit', 'PaymentMethod']], Union[str, 'LoanOrCredit', 'PaymentMethod'], None] = None
    includesObject: Union[List['TypeAndQuantityNode'], 'TypeAndQuantityNode', None] = None
    itemCondition: Union[List['OfferItemCondition'], 'OfferItemCondition', None] = None
    deliveryLeadTime: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    validThrough: Union[List[Union[datetime, date]], Union[datetime, date], None] = None