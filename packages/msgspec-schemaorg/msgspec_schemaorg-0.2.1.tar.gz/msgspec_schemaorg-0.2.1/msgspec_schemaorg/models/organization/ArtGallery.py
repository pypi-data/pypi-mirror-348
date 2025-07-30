from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.EntertainmentBusiness import EntertainmentBusiness
from typing import Optional, Union, Dict, List, Any


class ArtGallery(EntertainmentBusiness):
    """An art gallery."""
    type: str = field(default_factory=lambda: "ArtGallery", name="@type")