from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.AboutPage import AboutPage
    from msgspec_schemaorg.models.creativework.Article import Article
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.InteractionCounter import InteractionCounter
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
    from msgspec_schemaorg.models.intangible.MemberProgram import MemberProgram
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicy import MerchantReturnPolicy
    from msgspec_schemaorg.models.intangible.NonprofitType import NonprofitType
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferCatalog import OfferCatalog
    from msgspec_schemaorg.models.intangible.OwnershipInfo import OwnershipInfo
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.ProgramMembership import ProgramMembership
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.ShippingService import ShippingService
    from msgspec_schemaorg.models.intangible.VirtualLocation import VirtualLocation
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Organization(Thing):
    """An organization such as a school, NGO, corporation, club, etc."""
    type: str = field(default_factory=lambda: "Organization", name="@type")
    member: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    award: Union[List[str], str, None] = None
    isicV4: Union[List[str], str, None] = None
    agentInteractionStatistic: Union[List['InteractionCounter'], 'InteractionCounter', None] = None
    serviceArea: Union[List[Union['Place', 'AdministrativeArea', 'GeoShape']], Union['Place', 'AdministrativeArea', 'GeoShape'], None] = None
    alumni: Union[List['Person'], 'Person', None] = None
    diversityPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    reviews: Union[List['Review'], 'Review', None] = None
    duns: Union[List[str], str, None] = None
    review: Union[List['Review'], 'Review', None] = None
    members: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    email: Union[List[str], str, None] = None
    keywords: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    founders: Union[List['Person'], 'Person', None] = None
    publishingPrinciples: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    unnamedSourcesPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    funding: Union[List['Grant'], 'Grant', None] = None
    memberOf: Union[List[Union['ProgramMembership', 'MemberProgramTier', 'Organization']], Union['ProgramMembership', 'MemberProgramTier', 'Organization'], None] = None
    dissolutionDate: Union[List[date], date, None] = None
    hasShippingService: Union[List['ShippingService'], 'ShippingService', None] = None
    skills: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    nonprofitStatus: Union[List['NonprofitType'], 'NonprofitType', None] = None
    employee: Union[List['Person'], 'Person', None] = None
    founder: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    naics: Union[List[str], str, None] = None
    awards: Union[List[str], str, None] = None
    interactionStatistic: Union[List['InteractionCounter'], 'InteractionCounter', None] = None
    telephone: Union[List[str], str, None] = None
    legalRepresentative: Union[List['Person'], 'Person', None] = None
    actionableFeedbackPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    event: Union[List['Event'], 'Event', None] = None
    ownershipFundingInfo: Union[List[Union['URL', str, 'AboutPage', 'CreativeWork']], Union['URL', str, 'AboutPage', 'CreativeWork'], None] = None
    foundingDate: Union[List[date], date, None] = None
    legalName: Union[List[str], str, None] = None
    knowsAbout: Union[List[Union['URL', str, 'Thing']], Union['URL', str, 'Thing'], None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    iso6523Code: Union[List[str], str, None] = None
    employees: Union[List['Person'], 'Person', None] = None
    numberOfEmployees: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    foundingLocation: Union[List['Place'], 'Place', None] = None
    address: Union[List[Union[str, 'PostalAddress']], Union[str, 'PostalAddress'], None] = None
    contactPoints: Union[List['ContactPoint'], 'ContactPoint', None] = None
    events: Union[List['Event'], 'Event', None] = None
    department: Union[List['Organization'], 'Organization', None] = None
    hasPOS: Union[List['Place'], 'Place', None] = None
    globalLocationNumber: Union[List[str], str, None] = None
    leiCode: Union[List[str], str, None] = None
    taxID: Union[List[str], str, None] = None
    hasMerchantReturnPolicy: Union[List['MerchantReturnPolicy'], 'MerchantReturnPolicy', None] = None
    legalAddress: Union[List['PostalAddress'], 'PostalAddress', None] = None
    correctionsPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    hasGS1DigitalLink: Union[List['URL'], 'URL', None] = None
    makesOffer: Union[List['Offer'], 'Offer', None] = None
    parentOrganization: Union[List['Organization'], 'Organization', None] = None
    hasMemberProgram: Union[List['MemberProgram'], 'MemberProgram', None] = None
    slogan: Union[List[str], str, None] = None
    contactPoint: Union[List['ContactPoint'], 'ContactPoint', None] = None
    location: Union[List[Union[str, 'VirtualLocation', 'PostalAddress', 'Place']], Union[str, 'VirtualLocation', 'PostalAddress', 'Place'], None] = None
    vatID: Union[List[str], str, None] = None
    seeks: Union[List['Demand'], 'Demand', None] = None
    sponsor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    funder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    diversityStaffingReport: Union[List[Union['URL', 'Article']], Union['URL', 'Article'], None] = None
    companyRegistration: Union[List['Certification'], 'Certification', None] = None
    subOrganization: Union[List['Organization'], 'Organization', None] = None
    owns: Union[List[Union['Product', 'OwnershipInfo']], Union['Product', 'OwnershipInfo'], None] = None
    logo: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    acceptedPaymentMethod: Union[List[Union[str, 'LoanOrCredit', 'PaymentMethod']], Union[str, 'LoanOrCredit', 'PaymentMethod'], None] = None
    faxNumber: Union[List[str], str, None] = None
    ethicsPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    hasCredential: Union[List['EducationalOccupationalCredential'], 'EducationalOccupationalCredential', None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    hasCertification: Union[List['Certification'], 'Certification', None] = None
    brand: Union[List[Union['Brand', 'Organization']], Union['Brand', 'Organization'], None] = None
    knowsLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    hasOfferCatalog: Union[List['OfferCatalog'], 'OfferCatalog', None] = None