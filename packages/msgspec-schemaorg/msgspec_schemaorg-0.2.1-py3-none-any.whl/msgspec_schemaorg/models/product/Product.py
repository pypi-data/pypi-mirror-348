from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.creativework.WebContent import WebContent
    from msgspec_schemaorg.enums.intangible.AdultOrientedEnumeration import AdultOrientedEnumeration
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.EnergyConsumptionDetails import EnergyConsumptionDetails
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.intangible.Mass import Mass
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicy import MerchantReturnPolicy
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.enums.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.enums.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.intangible.SizeSpecification import SizeSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.Country import Country
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.product.ProductGroup import ProductGroup
    from msgspec_schemaorg.models.product.ProductModel import ProductModel
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Product(Thing):
    """Any offered product or service. For example: a pair of shoes; a concert ticket; the rental of a car; a haircut; or an episode of a TV show streamed online."""
    type: str = field(default_factory=lambda: "Product", name="@type")
    color: Union[List[str], str, None] = None
    award: Union[List[str], str, None] = None
    gtin8: Union[List[str], str, None] = None
    isRelatedTo: Union[List[Union['Service', 'Product']], Union['Service', 'Product'], None] = None
    asin: Union[List[Union['URL', str]], Union['URL', str], None] = None
    reviews: Union[List['Review'], 'Review', None] = None
    hasEnergyConsumptionDetails: Union[List['EnergyConsumptionDetails'], 'EnergyConsumptionDetails', None] = None
    manufacturer: Union[List['Organization'], 'Organization', None] = None
    offers: Union[List[Union['Demand', 'Offer']], Union['Demand', 'Offer'], None] = None
    review: Union[List['Review'], 'Review', None] = None
    countryOfAssembly: Union[List[str], str, None] = None
    mobileUrl: Union[List[str], str, None] = None
    countryOfLastProcessing: Union[List[str], str, None] = None
    keywords: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    colorSwatch: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    funding: Union[List['Grant'], 'Grant', None] = None
    height: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    awards: Union[List[str], str, None] = None
    inProductGroupWithID: Union[List[str], str, None] = None
    isFamilyFriendly: Union[List[bool], bool, None] = None
    mpn: Union[List[str], str, None] = None
    productionDate: Union[List[date], date, None] = None
    additionalProperty: Union[List['PropertyValue'], 'PropertyValue', None] = None
    gtin12: Union[List[str], str, None] = None
    size: Union[List[Union[str, 'DefinedTerm', 'SizeSpecification', 'QuantitativeValue']], Union[str, 'DefinedTerm', 'SizeSpecification', 'QuantitativeValue'], None] = None
    gtin13: Union[List[str], str, None] = None
    isVariantOf: Union[List[Union['ProductModel', 'ProductGroup']], Union['ProductModel', 'ProductGroup'], None] = None
    purchaseDate: Union[List[date], date, None] = None
    isAccessoryOrSparePartFor: Union[List['Product'], 'Product', None] = None
    hasMerchantReturnPolicy: Union[List['MerchantReturnPolicy'], 'MerchantReturnPolicy', None] = None
    hasGS1DigitalLink: Union[List['URL'], 'URL', None] = None
    material: Union[List[Union['URL', str, 'Product']], Union['URL', str, 'Product'], None] = None
    slogan: Union[List[str], str, None] = None
    gtin: Union[List[Union['URL', str]], Union['URL', str], None] = None
    width: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    countryOfOrigin: Union[List['Country'], 'Country', None] = None
    hasAdultConsideration: Union[List['AdultOrientedEnumeration'], 'AdultOrientedEnumeration', None] = None
    sku: Union[List[str], str, None] = None
    model: Union[List[Union[str, 'ProductModel']], Union[str, 'ProductModel'], None] = None
    negativeNotes: Union[List[Union[str, 'ListItem', 'WebContent', 'ItemList']], Union[str, 'ListItem', 'WebContent', 'ItemList'], None] = None
    category: Union[List[Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode']], Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode'], None] = None
    audience: Union[List['Audience'], 'Audience', None] = None
    gtin14: Union[List[str], str, None] = None
    depth: Union[List[Union['QuantitativeValue', 'Distance']], Union['QuantitativeValue', 'Distance'], None] = None
    logo: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    releaseDate: Union[List[date], date, None] = None
    productID: Union[List[str], str, None] = None
    weight: Union[List[Union['Mass', 'QuantitativeValue']], Union['Mass', 'QuantitativeValue'], None] = None
    nsn: Union[List[str], str, None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    itemCondition: Union[List['OfferItemCondition'], 'OfferItemCondition', None] = None
    hasCertification: Union[List['Certification'], 'Certification', None] = None
    brand: Union[List[Union['Brand', 'Organization']], Union['Brand', 'Organization'], None] = None
    positiveNotes: Union[List[Union[str, 'ListItem', 'ItemList', 'WebContent']], Union[str, 'ListItem', 'ItemList', 'WebContent'], None] = None
    isSimilarTo: Union[List[Union['Product', 'Service']], Union['Product', 'Service'], None] = None
    pattern: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    isConsumableFor: Union[List['Product'], 'Product', None] = None
    hasMeasurement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None