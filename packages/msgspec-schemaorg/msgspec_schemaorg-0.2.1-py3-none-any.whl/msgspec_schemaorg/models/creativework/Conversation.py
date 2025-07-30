from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Conversation(CreativeWork):
    """One or more messages between organizations or people on a particular topic. Individual messages can be linked to the conversation with isPartOf or hasPart properties."""
    type: str = field(default_factory=lambda: "Conversation", name="@type")