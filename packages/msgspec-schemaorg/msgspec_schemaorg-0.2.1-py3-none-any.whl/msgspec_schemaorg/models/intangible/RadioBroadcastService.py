from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.BroadcastService import BroadcastService
from typing import Optional, Union, Dict, List, Any


class RadioBroadcastService(BroadcastService):
    """A delivery service through which radio content is provided via broadcast over the air or online."""
    type: str = field(default_factory=lambda: "RadioBroadcastService", name="@type")