from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.WebPageElement import WebPageElement
    from msgspec_schemaorg.models.intangible.BreadcrumbList import BreadcrumbList
    from msgspec_schemaorg.models.intangible.SpeakableSpecification import SpeakableSpecification
    from msgspec_schemaorg.models.intangible.Specialty import Specialty
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date
from typing import Optional, Union, Dict, List, Any


class WebPage(CreativeWork):
    """A web page. Every web page is implicitly assumed to be declared to be of type WebPage, so the various properties about that webpage, such as <code>breadcrumb</code> may be used. We recommend explicit declaration if these properties are specified, but if they are found outside of an itemscope, they will be assumed to be about the page."""
    type: str = field(default_factory=lambda: "WebPage", name="@type")
    mainContentOfPage: Union[List['WebPageElement'], 'WebPageElement', None] = None
    specialty: Union[List['Specialty'], 'Specialty', None] = None
    significantLink: Union[List['URL'], 'URL', None] = None
    relatedLink: Union[List['URL'], 'URL', None] = None
    primaryImageOfPage: Union[List['ImageObject'], 'ImageObject', None] = None
    significantLinks: Union[List['URL'], 'URL', None] = None
    breadcrumb: Union[List[Union[str, 'BreadcrumbList']], Union[str, 'BreadcrumbList'], None] = None
    reviewedBy: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    speakable: Union[List[Union['URL', 'SpeakableSpecification']], Union['URL', 'SpeakableSpecification'], None] = None
    lastReviewed: Union[List[date], date, None] = None