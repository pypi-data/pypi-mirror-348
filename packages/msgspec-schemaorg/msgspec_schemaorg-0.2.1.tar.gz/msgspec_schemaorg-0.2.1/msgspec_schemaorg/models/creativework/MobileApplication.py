from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.SoftwareApplication import SoftwareApplication
from typing import Optional, Union, Dict, List, Any


class MobileApplication(SoftwareApplication):
    """A software application designed specifically to work well on a mobile device such as a telephone."""
    type: str = field(default_factory=lambda: "MobileApplication", name="@type")
    carrierRequirements: Union[List[str], str, None] = None