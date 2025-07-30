from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.enums.intangible.CertificationStatusEnumeration import CertificationStatusEnumeration
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Rating import Rating
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Certification(CreativeWork):
    """A Certification is an official and authoritative statement about a subject, for example a product, service, person, or organization. A certification is typically issued by an indendent certification body, for example a professional organization or government. It formally attests certain characteristics about the subject, for example Organizations can be ISO certified, Food products can be certified Organic or Vegan, a Person can be a certified professional, a Place can be certified for food processing. There are certifications for many domains: regulatory, organizational, recycling, food, efficiency, educational, ecological, etc. A certification is a form of credential, as are accreditations and licenses. Mapped from the [gs1:CertificationDetails](https://www.gs1.org/voc/CertificationDetails) class in the GS1 Web Vocabulary."""
    type: str = field(default_factory=lambda: "Certification", name="@type")
    issuedBy: Union[List['Organization'], 'Organization', None] = None
    about: Union[List['Thing'], 'Thing', None] = None
    auditDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    certificationIdentification: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    datePublished: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    expires: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    certificationStatus: Union[List['CertificationStatusEnumeration'], 'CertificationStatusEnumeration', None] = None
    certificationRating: Union[List['Rating'], 'Rating', None] = None
    logo: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    hasMeasurement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    validIn: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None