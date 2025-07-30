from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class LiteraryEvent(Event):
    """Event type: Literary event."""
    type: str = field(default_factory=lambda: "LiteraryEvent", name="@type")