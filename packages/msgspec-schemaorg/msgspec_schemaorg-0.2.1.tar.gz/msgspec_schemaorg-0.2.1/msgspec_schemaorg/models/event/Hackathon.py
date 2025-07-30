from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class Hackathon(Event):
    """A [hackathon](https://en.wikipedia.org/wiki/Hackathon) event."""
    type: str = field(default_factory=lambda: "Hackathon", name="@type")