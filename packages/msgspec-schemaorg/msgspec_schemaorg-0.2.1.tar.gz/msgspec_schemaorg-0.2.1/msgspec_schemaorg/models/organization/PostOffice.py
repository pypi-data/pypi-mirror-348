from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.GovernmentOffice import GovernmentOffice
from typing import Optional, Union, Dict, List, Any


class PostOffice(GovernmentOffice):
    """A post office."""
    type: str = field(default_factory=lambda: "PostOffice", name="@type")