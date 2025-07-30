from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
    from msgspec_schemaorg.models.intangible.ComputerLanguage import ComputerLanguage
from typing import Optional, Union, Dict, List, Any


class SoftwareSourceCode(CreativeWork):
    """Computer programming source code. Example: Full (compile ready) solutions, code snippet samples, scripts, templates."""
    type: str = field(default_factory=lambda: "SoftwareSourceCode", name="@type")
    targetProduct: Union[List['SoftwareApplication'], 'SoftwareApplication', None] = None
    runtime: Union[List[str], str, None] = None
    runtimePlatform: Union[List[str], str, None] = None
    codeRepository: Union[List['URL'], 'URL', None] = None
    sampleType: Union[List[str], str, None] = None
    programmingLanguage: Union[List[Union[str, 'ComputerLanguage']], Union[str, 'ComputerLanguage'], None] = None
    codeSampleType: Union[List[str], str, None] = None