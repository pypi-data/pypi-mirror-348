from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class Consortium(Organization):
    """A Consortium is a membership [[Organization]] whose members are typically Organizations."""
    type: str = field(default_factory=lambda: "Consortium", name="@type")