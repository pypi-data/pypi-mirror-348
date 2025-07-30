from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.AudioObject import AudioObject
    from msgspec_schemaorg.models.creativework.Claim import Claim
    from msgspec_schemaorg.models.creativework.Clip import Clip
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.models.creativework.CorrectionComment import CorrectionComment
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.creativework.WebPage import WebPage
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.event.PublicationEvent import PublicationEvent
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.AlignmentObject import AlignmentObject
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.enums.intangible.IPTCDigitalSourceEnumeration import IPTCDigitalSourceEnumeration
    from msgspec_schemaorg.models.intangible.InteractionCounter import InteractionCounter
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Rating import Rating
    from msgspec_schemaorg.models.intangible.SizeSpecification import SizeSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Country import Country
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class CreativeWork(Thing):
    """The most generic kind of creative work, including books, movies, photographs, software programs, etc."""
    type: str = field(default_factory=lambda: "CreativeWork", name="@type")
    hasPart: Union[List['CreativeWork'], 'CreativeWork', None] = None
    award: Union[List[str], str, None] = None
    accessModeSufficient: Union[List['ItemList'], 'ItemList', None] = None
    reviews: Union[List['Review'], 'Review', None] = None
    dateModified: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    offers: Union[List[Union['Demand', 'Offer']], Union['Demand', 'Offer'], None] = None
    contentLocation: Union[List['Place'], 'Place', None] = None
    review: Union[List['Review'], 'Review', None] = None
    contentRating: Union[List[Union[str, 'Rating']], Union[str, 'Rating'], None] = None
    accessibilityControl: Union[List[str], str, None] = None
    releasedEvent: Union[List['PublicationEvent'], 'PublicationEvent', None] = None
    contributor: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    educationalAlignment: Union[List['AlignmentObject'], 'AlignmentObject', None] = None
    translator: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    about: Union[List['Thing'], 'Thing', None] = None
    copyrightNotice: Union[List[str], str, None] = None
    typicalAgeRange: Union[List[str], str, None] = None
    keywords: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    publishingPrinciples: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    funding: Union[List['Grant'], 'Grant', None] = None
    encodings: Union[List['MediaObject'], 'MediaObject', None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    isPartOf: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    encoding: Union[List['MediaObject'], 'MediaObject', None] = None
    video: Union[List[Union['Clip', 'VideoObject']], Union['Clip', 'VideoObject'], None] = None
    thumbnail: Union[List['ImageObject'], 'ImageObject', None] = None
    discussionUrl: Union[List['URL'], 'URL', None] = None
    interactivityType: Union[List[str], str, None] = None
    timeRequired: Union[List['Duration'], 'Duration', None] = None
    text: Union[List[str], str, None] = None
    isBasedOn: Union[List[Union['URL', 'CreativeWork', 'Product']], Union['URL', 'CreativeWork', 'Product'], None] = None
    awards: Union[List[str], str, None] = None
    interactionStatistic: Union[List['InteractionCounter'], 'InteractionCounter', None] = None
    conditionsOfAccess: Union[List[str], str, None] = None
    temporalCoverage: Union[List[Union[datetime, 'URL', str]], Union[datetime, 'URL', str], None] = None
    version: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    encodingFormat: Union[List[Union['URL', str]], Union['URL', str], None] = None
    publication: Union[List['PublicationEvent'], 'PublicationEvent', None] = None
    isFamilyFriendly: Union[List[bool], bool, None] = None
    materialExtent: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None
    headline: Union[List[str], str, None] = None
    accessMode: Union[List[str], str, None] = None
    accountablePerson: Union[List['Person'], 'Person', None] = None
    accessibilitySummary: Union[List[str], str, None] = None
    educationalUse: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    workExample: Union[List['CreativeWork'], 'CreativeWork', None] = None
    editor: Union[List['Person'], 'Person', None] = None
    schemaVersion: Union[List[Union['URL', str]], Union['URL', str], None] = None
    size: Union[List[Union[str, 'DefinedTerm', 'SizeSpecification', 'QuantitativeValue']], Union[str, 'DefinedTerm', 'SizeSpecification', 'QuantitativeValue'], None] = None
    assesses: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    audio: Union[List[Union['MusicRecording', 'AudioObject', 'Clip']], Union['MusicRecording', 'AudioObject', 'Clip'], None] = None
    associatedMedia: Union[List['MediaObject'], 'MediaObject', None] = None
    author: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    mentions: Union[List['Thing'], 'Thing', None] = None
    fileFormat: Union[List[Union['URL', str]], Union['URL', str], None] = None
    spatialCoverage: Union[List['Place'], 'Place', None] = None
    wordCount: Union[List[int], int, None] = None
    isAccessibleForFree: Union[List[bool], bool, None] = None
    contentReferenceTime: Union[List[datetime], datetime, None] = None
    position: Union[List[Union[int, str]], Union[int, str], None] = None
    exampleOfWork: Union[List['CreativeWork'], 'CreativeWork', None] = None
    datePublished: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    material: Union[List[Union['URL', str, 'Product']], Union['URL', str, 'Product'], None] = None
    producer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    abstract: Union[List[str], str, None] = None
    acquireLicensePage: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    usageInfo: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    expires: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    mainEntity: Union[List['Thing'], 'Thing', None] = None
    copyrightHolder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    alternativeHeadline: Union[List[str], str, None] = None
    creator: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    countryOfOrigin: Union[List['Country'], 'Country', None] = None
    teaches: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    educationalLevel: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    digitalSourceType: Union[List['IPTCDigitalSourceEnumeration'], 'IPTCDigitalSourceEnumeration', None] = None
    recordedAt: Union[List['Event'], 'Event', None] = None
    learningResourceType: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    workTranslation: Union[List['CreativeWork'], 'CreativeWork', None] = None
    isBasedOnUrl: Union[List[Union['URL', 'CreativeWork', 'Product']], Union['URL', 'CreativeWork', 'Product'], None] = None
    publisherImprint: Union[List['Organization'], 'Organization', None] = None
    sponsor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    creativeWorkStatus: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    audience: Union[List['Audience'], 'Audience', None] = None
    thumbnailUrl: Union[List['URL'], 'URL', None] = None
    funder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    creditText: Union[List[str], str, None] = None
    copyrightYear: Union[List[int | float], int | float, None] = None
    translationOfWork: Union[List['CreativeWork'], 'CreativeWork', None] = None
    sourceOrganization: Union[List['Organization'], 'Organization', None] = None
    locationCreated: Union[List['Place'], 'Place', None] = None
    accessibilityAPI: Union[List[str], str, None] = None
    correction: Union[List[Union['URL', str, 'CorrectionComment']], Union['URL', str, 'CorrectionComment'], None] = None
    sdDatePublished: Union[List[date], date, None] = None
    character: Union[List['Person'], 'Person', None] = None
    archivedAt: Union[List[Union['URL', 'WebPage']], Union['URL', 'WebPage'], None] = None
    spatial: Union[List['Place'], 'Place', None] = None
    accessibilityFeature: Union[List[str], str, None] = None
    sdPublisher: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    sdLicense: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    license: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    editEIDR: Union[List[Union['URL', str]], Union['URL', str], None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    dateCreated: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    accessibilityHazard: Union[List[str], str, None] = None
    publisher: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    citation: Union[List[Union[str, 'CreativeWork']], Union[str, 'CreativeWork'], None] = None
    genre: Union[List[Union['URL', str]], Union['URL', str], None] = None
    maintainer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    pattern: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    temporal: Union[List[Union[datetime, str]], Union[datetime, str], None] = None
    comment: Union[List['Comment'], 'Comment', None] = None
    commentCount: Union[List[int], int, None] = None
    interpretedAsClaim: Union[List['Claim'], 'Claim', None] = None