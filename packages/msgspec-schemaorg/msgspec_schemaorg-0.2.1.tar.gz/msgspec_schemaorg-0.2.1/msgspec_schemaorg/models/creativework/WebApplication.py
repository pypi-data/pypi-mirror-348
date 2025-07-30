from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
from typing import Optional, Union, Dict, List, Any


class WebApplication(SoftwareApplication):
    """Web applications."""
    type: str = field(default_factory=lambda: "WebApplication", name="@type")
    browserRequirements: Union[List[str], str, None] = None