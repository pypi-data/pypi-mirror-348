from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.PostalAddress import PostalAddress
    from msgspec_schemaorg.models.intangible.Service import Service
    from msgspec_schemaorg.models.place.Place import Place
from typing import Optional, Union, Dict, List, Any


class ServiceChannel(Intangible):
    """A means for accessing a service, e.g. a government office location, web site, or phone number."""
    type: str = field(default_factory=lambda: "ServiceChannel", name="@type")
    providesService: Union[List['Service'], 'Service', None] = None
    servicePhone: Union[List['ContactPoint'], 'ContactPoint', None] = None
    serviceUrl: Union[List['URL'], 'URL', None] = None
    processingTime: Union[List['Duration'], 'Duration', None] = None
    servicePostalAddress: Union[List['PostalAddress'], 'PostalAddress', None] = None
    availableLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    serviceLocation: Union[List['Place'], 'Place', None] = None
    serviceSmsNumber: Union[List['ContactPoint'], 'ContactPoint', None] = None