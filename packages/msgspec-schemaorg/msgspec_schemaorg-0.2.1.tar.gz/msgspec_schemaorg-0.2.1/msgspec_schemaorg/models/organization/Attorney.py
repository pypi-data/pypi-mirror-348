from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LegalService import LegalService
from typing import Optional, Union, Dict, List, Any


class Attorney(LegalService):
    """Professional service: Attorney. \\n\\nThis type is deprecated - [[LegalService]] is more inclusive and less ambiguous."""
    type: str = field(default_factory=lambda: "Attorney", name="@type")