from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class MusicEvent(Event):
    """Event type: Music event."""
    type: str = field(default_factory=lambda: "MusicEvent", name="@type")