from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LegalService import LegalService
from typing import Optional, Union, Dict, List, Any


class Notary(LegalService):
    """A notary."""
    type: str = field(default_factory=lambda: "Notary", name="@type")