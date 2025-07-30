from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.PublicationEvent import PublicationEvent
from typing import Optional, Union, Dict, List, Any


class OnDemandEvent(PublicationEvent):
    """A publication event, e.g. catch-up TV or radio podcast, during which a program is available on-demand."""
    type: str = field(default_factory=lambda: "OnDemandEvent", name="@type")