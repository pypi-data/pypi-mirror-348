from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.enums.intangible.EventAttendanceModeEnumeration import EventAttendanceModeEnumeration
    from msgspec_schemaorg.enums.intangible.EventStatusType import EventStatusType
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Schedule import Schedule
    from msgspec_schemaorg.models.intangible.VirtualLocation import VirtualLocation
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class Event(Thing):
    """An event happening at a certain time and location, such as a concert, lecture, or festival. Ticketing information may be added via the [[offers]] property. Repeated events may be structured as separate Event objects."""
    type: str = field(default_factory=lambda: "Event", name="@type")
    superEvent: Union[List['Event'], 'Event', None] = None
    performers: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    subEvent: Union[List['Event'], 'Event', None] = None
    eventStatus: Union[List['EventStatusType'], 'EventStatusType', None] = None
    maximumPhysicalAttendeeCapacity: Union[List[int], int, None] = None
    workFeatured: Union[List['CreativeWork'], 'CreativeWork', None] = None
    remainingAttendeeCapacity: Union[List[int], int, None] = None
    offers: Union[List[Union['Demand', 'Offer']], Union['Demand', 'Offer'], None] = None
    review: Union[List['Review'], 'Review', None] = None
    attendee: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    contributor: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    translator: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    performer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    maximumAttendeeCapacity: Union[List[int], int, None] = None
    about: Union[List['Thing'], 'Thing', None] = None
    typicalAgeRange: Union[List[str], str, None] = None
    actor: Union[List[Union['PerformingGroup', 'Person']], Union['PerformingGroup', 'Person'], None] = None
    keywords: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    funding: Union[List['Grant'], 'Grant', None] = None
    recordedIn: Union[List['CreativeWork'], 'CreativeWork', None] = None
    director: Union[List['Person'], 'Person', None] = None
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    doorTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    isAccessibleForFree: Union[List[bool], bool, None] = None
    location: Union[List[Union[str, 'VirtualLocation', 'PostalAddress', 'Place']], Union[str, 'VirtualLocation', 'PostalAddress', 'Place'], None] = None
    previousStartDate: Union[List[date], date, None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    organizer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    workPerformed: Union[List['CreativeWork'], 'CreativeWork', None] = None
    sponsor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    eventAttendanceMode: Union[List['EventAttendanceModeEnumeration'], 'EventAttendanceModeEnumeration', None] = None
    audience: Union[List['Audience'], 'Audience', None] = None
    subEvents: Union[List['Event'], 'Event', None] = None
    maximumVirtualAttendeeCapacity: Union[List[int], int, None] = None
    funder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    attendees: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    eventSchedule: Union[List['Schedule'], 'Schedule', None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None
    composer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None