from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.enums.intangible.GovernmentBenefitsType import GovernmentBenefitsType
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferCatalog import OfferCatalog
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
    from msgspec_schemaorg.enums.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.intangible.ServiceChannel import ServiceChannel
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class Service(Intangible):
    """A service provided by an organization, e.g. delivery service, print services, etc."""
    type: str = field(default_factory=lambda: "Service", name="@type")
    award: Union[List[str], str, None] = None
    isRelatedTo: Union[List[Union['Service', 'Product']], Union['Service', 'Product'], None] = None
    serviceOutput: Union[List['Thing'], 'Thing', None] = None
    serviceArea: Union[List[Union['Place', 'AdministrativeArea', 'GeoShape']], Union['Place', 'AdministrativeArea', 'GeoShape'], None] = None
    offers: Union[List[Union['Demand', 'Offer']], Union['Demand', 'Offer'], None] = None
    review: Union[List['Review'], 'Review', None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    termsOfService: Union[List[Union['URL', str]], Union['URL', str], None] = None
    providerMobility: Union[List[str], str, None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    produces: Union[List['Thing'], 'Thing', None] = None
    availableChannel: Union[List['ServiceChannel'], 'ServiceChannel', None] = None
    serviceType: Union[List[Union[str, 'GovernmentBenefitsType']], Union[str, 'GovernmentBenefitsType'], None] = None
    slogan: Union[List[str], str, None] = None
    broker: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    serviceAudience: Union[List['Audience'], 'Audience', None] = None
    category: Union[List[Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode']], Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode'], None] = None
    audience: Union[List['Audience'], 'Audience', None] = None
    logo: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    hoursAvailable: Union[List['OpeningHoursSpecification'], 'OpeningHoursSpecification', None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    hasCertification: Union[List['Certification'], 'Certification', None] = None
    brand: Union[List[Union['Brand', 'Organization']], Union['Brand', 'Organization'], None] = None
    hasOfferCatalog: Union[List['OfferCatalog'], 'OfferCatalog', None] = None
    isSimilarTo: Union[List[Union['Product', 'Service']], Union['Product', 'Service'], None] = None