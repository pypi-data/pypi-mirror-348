from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class GovernmentOffice(LocalBusiness):
    """A government office&#x2014;for example, an IRS or DMV office."""
    type: str = field(default_factory=lambda: "GovernmentOffice", name="@type")