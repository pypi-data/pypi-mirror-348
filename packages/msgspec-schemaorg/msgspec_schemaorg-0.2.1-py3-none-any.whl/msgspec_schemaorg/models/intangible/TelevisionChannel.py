from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.BroadcastChannel import BroadcastChannel
from typing import Optional, Union, Dict, List, Any


class TelevisionChannel(BroadcastChannel):
    """A unique instance of a television BroadcastService on a CableOrSatelliteService lineup."""
    type: str = field(default_factory=lambda: "TelevisionChannel", name="@type")