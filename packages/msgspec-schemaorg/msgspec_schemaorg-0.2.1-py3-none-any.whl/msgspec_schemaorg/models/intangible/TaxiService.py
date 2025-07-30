from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import Optional, Union, Dict, List, Any


class TaxiService(Service):
    """A service for a vehicle for hire with a driver for local travel. Fares are usually calculated based on distance traveled."""
    type: str = field(default_factory=lambda: "TaxiService", name="@type")