from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.OnlineBusiness import OnlineBusiness
from typing import Optional, Union, Dict, List, Any


class OnlineStore(OnlineBusiness):
    """An eCommerce site."""
    type: str = field(default_factory=lambda: "OnlineStore", name="@type")