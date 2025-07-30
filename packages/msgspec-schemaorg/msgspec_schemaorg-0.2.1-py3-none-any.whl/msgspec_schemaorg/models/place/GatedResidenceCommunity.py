from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.Residence import Residence
from typing import Optional, Union, Dict, List, Any


class GatedResidenceCommunity(Residence):
    """Residence type: Gated community."""
    type: str = field(default_factory=lambda: "GatedResidenceCommunity", name="@type")