from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class EmergencyService(LocalBusiness):
    """An emergency service, such as a fire station or ER."""
    type: str = field(default_factory=lambda: "EmergencyService", name="@type")