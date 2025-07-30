from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class OnlineBusiness(Organization):
    """A particular online business, either standalone or the online part of a broader organization. Examples include an eCommerce site, an online travel booking site, an online learning site, an online logistics and shipping provider, an online (virtual) doctor, etc."""
    type: str = field(default_factory=lambda: "OnlineBusiness", name="@type")