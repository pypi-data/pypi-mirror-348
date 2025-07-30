from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class SelfStorage(LocalBusiness):
    """A self-storage facility."""
    type: str = field(default_factory=lambda: "SelfStorage", name="@type")