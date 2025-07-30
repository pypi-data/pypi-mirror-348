from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.enums.intangible.AdultOrientedEnumeration import AdultOrientedEnumeration
    from msgspec_schemaorg.models.intangible.AggregateOffer import AggregateOffer
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.BusinessEntityType import BusinessEntityType
    from msgspec_schemaorg.models.intangible.BusinessFunction import BusinessFunction
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.enums.intangible.ItemAvailability import ItemAvailability
    from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MenuItem import MenuItem
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicy import MerchantReturnPolicy
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.enums.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.models.intangible.OfferShippingDetails import OfferShippingDetails
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.enums.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
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
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class Offer(Intangible):
    """An offer to transfer some rights to an item or to provide a service — for example, an offer to sell tickets to an event, to rent the DVD of a movie, to stream a TV show over the internet, to repair a motorcycle, or to loan a book.\\n\\nNote: As the [[businessFunction]] property, which identifies the form of offer (e.g. sell, lease, repair, dispose), defaults to http://purl.org/goodrelations/v1#Sell; an Offer without a defined businessFunction value can be assumed to be an offer to sell.\\n\\nFor [GTIN](http://www.gs1.org/barcodes/technical/idkeys/gtin)-related fields, see [Check Digit calculator](http://www.gs1.org/barcodes/support/check_digit_calculator) and [validation guide](http://www.gs1us.org/resources/standards/gtin-validation-guide) from [GS1](http://www.gs1.org/)."""
    type: str = field(default_factory=lambda: "Offer", name="@type")
    warranty: Union[List['WarrantyPromise'], 'WarrantyPromise', None] = None
    gtin8: Union[List[str], str, None] = None
    asin: Union[List[Union['URL', str]], Union['URL', str], None] = None
    reviews: Union[List['Review'], 'Review', None] = None
    eligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    eligibleTransactionVolume: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    review: Union[List['Review'], 'Review', None] = None
    availability: Union[List['ItemAvailability'], 'ItemAvailability', None] = None
    checkoutPageURLTemplate: Union[List[str], str, None] = None
    businessFunction: Union[List['BusinessFunction'], 'BusinessFunction', None] = None
    inventoryLevel: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    mobileUrl: Union[List[str], str, None] = None
    addOn: Union[List['Offer'], 'Offer', None] = None
    advanceBookingRequirement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    leaseLength: Union[List[Union['Duration', 'QuantitativeValue']], Union['Duration', 'QuantitativeValue'], None] = None
    eligibleDuration: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    priceValidUntil: Union[List[date], date, None] = None
    isFamilyFriendly: Union[List[bool], bool, None] = None
    availableAtOrFrom: Union[List['Place'], 'Place', None] = None
    priceCurrency: Union[List[str], str, None] = None
    seller: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    itemOffered: Union[List[Union['Service', 'AggregateOffer', 'CreativeWork', 'Event', 'MenuItem', 'Product', 'Trip']], Union['Service', 'AggregateOffer', 'CreativeWork', 'Event', 'MenuItem', 'Product', 'Trip'], None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    mpn: Union[List[str], str, None] = None
    additionalProperty: Union[List['PropertyValue'], 'PropertyValue', None] = None
    gtin12: Union[List[str], str, None] = None
    ineligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    eligibleQuantity: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    gtin13: Union[List[str], str, None] = None
    availabilityStarts: Union[List[Union[datetime, date, time]], Union[datetime, date, time], None] = None
    eligibleCustomerType: Union[List['BusinessEntityType'], 'BusinessEntityType', None] = None
    hasMerchantReturnPolicy: Union[List['MerchantReturnPolicy'], 'MerchantReturnPolicy', None] = None
    offeredBy: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    hasGS1DigitalLink: Union[List['URL'], 'URL', None] = None
    gtin: Union[List[Union['URL', str]], Union['URL', str], None] = None
    availabilityEnds: Union[List[Union[datetime, date, time]], Union[datetime, date, time], None] = None
    priceSpecification: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    hasAdultConsideration: Union[List['AdultOrientedEnumeration'], 'AdultOrientedEnumeration', None] = None
    sku: Union[List[str], str, None] = None
    category: Union[List[Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode']], Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode'], None] = None
    shippingDetails: Union[List['OfferShippingDetails'], 'OfferShippingDetails', None] = None
    price: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    gtin14: Union[List[str], str, None] = None
    serialNumber: Union[List[str], str, None] = None
    availableDeliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None
    acceptedPaymentMethod: Union[List[Union[str, 'LoanOrCredit', 'PaymentMethod']], Union[str, 'LoanOrCredit', 'PaymentMethod'], None] = None
    includesObject: Union[List['TypeAndQuantityNode'], 'TypeAndQuantityNode', None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    validForMemberTier: Union[List['MemberProgramTier'], 'MemberProgramTier', None] = None
    itemCondition: Union[List['OfferItemCondition'], 'OfferItemCondition', None] = None
    deliveryLeadTime: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    hasMeasurement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    validThrough: Union[List[Union[datetime, date]], Union[datetime, date], None] = None