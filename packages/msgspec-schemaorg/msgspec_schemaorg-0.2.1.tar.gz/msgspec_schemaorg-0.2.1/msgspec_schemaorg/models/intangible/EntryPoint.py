from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
    from msgspec_schemaorg.enums.intangible.DigitalPlatformEnumeration import DigitalPlatformEnumeration
from typing import Optional, Union, Dict, List, Any


class EntryPoint(Intangible):
    """An entry point, within some Web-based protocol."""
    type: str = field(default_factory=lambda: "EntryPoint", name="@type")
    httpMethod: Union[List[str], str, None] = None
    actionPlatform: Union[List[Union['URL', str, 'DigitalPlatformEnumeration']], Union['URL', str, 'DigitalPlatformEnumeration'], None] = None
    actionApplication: Union[List['SoftwareApplication'], 'SoftwareApplication', None] = None
    urlTemplate: Union[List[str], str, None] = None
    encodingType: Union[List[str], str, None] = None
    contentType: Union[List[str], str, None] = None
    application: Union[List['SoftwareApplication'], 'SoftwareApplication', None] = None