from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import Optional, Union, Dict, List, Any


class CableOrSatelliteService(Service):
    """A service which provides access to media programming like TV or radio. Access may be via cable or satellite."""
    type: str = field(default_factory=lambda: "CableOrSatelliteService", name="@type")