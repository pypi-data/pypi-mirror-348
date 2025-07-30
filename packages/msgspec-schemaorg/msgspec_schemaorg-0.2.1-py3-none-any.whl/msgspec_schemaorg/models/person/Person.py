from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Certification import Certification
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.Brand import Brand
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.enums.intangible.GenderType import GenderType
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.InteractionCounter import InteractionCounter
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.Mass import Mass
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.Occupation import Occupation
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.OfferCatalog import OfferCatalog
    from msgspec_schemaorg.models.intangible.OwnershipInfo import OwnershipInfo
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.intangible.ProgramMembership import ProgramMembership
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Country import Country
    from msgspec_schemaorg.models.place.EducationalOrganization import EducationalOrganization
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Person(Thing):
    """A person (alive, dead, undead, or fictional)."""
    type: str = field(default_factory=lambda: "Person", name="@type")
    jobTitle: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    award: Union[List[str], str, None] = None
    isicV4: Union[List[str], str, None] = None
    agentInteractionStatistic: Union[List['InteractionCounter'], 'InteractionCounter', None] = None
    duns: Union[List[str], str, None] = None
    colleague: Union[List[Union['URL', 'Person']], Union['URL', 'Person'], None] = None
    additionalName: Union[List[str], str, None] = None
    email: Union[List[str], str, None] = None
    parents: Union[List['Person'], 'Person', None] = None
    parent: Union[List['Person'], 'Person', None] = None
    gender: Union[List[Union[str, 'GenderType']], Union[str, 'GenderType'], None] = None
    publishingPrinciples: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    colleagues: Union[List['Person'], 'Person', None] = None
    funding: Union[List['Grant'], 'Grant', None] = None
    memberOf: Union[List[Union['ProgramMembership', 'MemberProgramTier', 'Organization']], Union['ProgramMembership', 'MemberProgramTier', 'Organization'], None] = None
    worksFor: Union[List['Organization'], 'Organization', None] = None
    height: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    skills: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    givenName: Union[List[str], str, None] = None
    naics: Union[List[str], str, None] = None
    awards: Union[List[str], str, None] = None
    interactionStatistic: Union[List['InteractionCounter'], 'InteractionCounter', None] = None
    telephone: Union[List[str], str, None] = None
    netWorth: Union[List[Union['PriceSpecification', 'MonetaryAmount']], Union['PriceSpecification', 'MonetaryAmount'], None] = None
    deathDate: Union[List[date], date, None] = None
    affiliation: Union[List['Organization'], 'Organization', None] = None
    workLocation: Union[List[Union['ContactPoint', 'Place']], Union['ContactPoint', 'Place'], None] = None
    siblings: Union[List['Person'], 'Person', None] = None
    knowsAbout: Union[List[Union['URL', str, 'Thing']], Union['URL', str, 'Thing'], None] = None
    pronouns: Union[List[Union[str, 'StructuredValue', 'DefinedTerm']], Union[str, 'StructuredValue', 'DefinedTerm'], None] = None
    address: Union[List[Union[str, 'PostalAddress']], Union[str, 'PostalAddress'], None] = None
    performerIn: Union[List['Event'], 'Event', None] = None
    contactPoints: Union[List['ContactPoint'], 'ContactPoint', None] = None
    hasPOS: Union[List['Place'], 'Place', None] = None
    globalLocationNumber: Union[List[str], str, None] = None
    taxID: Union[List[str], str, None] = None
    children: Union[List['Person'], 'Person', None] = None
    makesOffer: Union[List['Offer'], 'Offer', None] = None
    hasOccupation: Union[List['Occupation'], 'Occupation', None] = None
    contactPoint: Union[List['ContactPoint'], 'ContactPoint', None] = None
    birthPlace: Union[List['Place'], 'Place', None] = None
    sibling: Union[List['Person'], 'Person', None] = None
    vatID: Union[List[str], str, None] = None
    seeks: Union[List['Demand'], 'Demand', None] = None
    sponsor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    relatedTo: Union[List['Person'], 'Person', None] = None
    knows: Union[List['Person'], 'Person', None] = None
    spouse: Union[List['Person'], 'Person', None] = None
    honorificSuffix: Union[List[str], str, None] = None
    nationality: Union[List['Country'], 'Country', None] = None
    funder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    birthDate: Union[List[date], date, None] = None
    owns: Union[List[Union['Product', 'OwnershipInfo']], Union['Product', 'OwnershipInfo'], None] = None
    alumniOf: Union[List[Union['EducationalOrganization', 'Organization']], Union['EducationalOrganization', 'Organization'], None] = None
    weight: Union[List[Union['Mass', 'QuantitativeValue']], Union['Mass', 'QuantitativeValue'], None] = None
    faxNumber: Union[List[str], str, None] = None
    hasCredential: Union[List['EducationalOccupationalCredential'], 'EducationalOccupationalCredential', None] = None
    follows: Union[List['Person'], 'Person', None] = None
    familyName: Union[List[str], str, None] = None
    callSign: Union[List[str], str, None] = None
    hasCertification: Union[List['Certification'], 'Certification', None] = None
    brand: Union[List[Union['Brand', 'Organization']], Union['Brand', 'Organization'], None] = None
    knowsLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    hasOfferCatalog: Union[List['OfferCatalog'], 'OfferCatalog', None] = None
    honorificPrefix: Union[List[str], str, None] = None
    deathPlace: Union[List['Place'], 'Place', None] = None
    homeLocation: Union[List[Union['ContactPoint', 'Place']], Union['ContactPoint', 'Place'], None] = None