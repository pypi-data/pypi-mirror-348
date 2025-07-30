from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class TheaterEvent(Event):
    """Event type: Theater performance."""
    type: str = field(default_factory=lambda: "TheaterEvent", name="@type")