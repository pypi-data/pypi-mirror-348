from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class LibrarySystem(Organization):
    """A [[LibrarySystem]] is a collaborative system amongst several libraries."""
    type: str = field(default_factory=lambda: "LibrarySystem", name="@type")