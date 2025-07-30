from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class Festival(Event):
    """Event type: Festival."""
    type: str = field(default_factory=lambda: "Festival", name="@type")