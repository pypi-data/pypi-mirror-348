from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Message import Message
from typing import Optional, Union, Dict, List, Any


class EmailMessage(Message):
    """An email message."""
    type: str = field(default_factory=lambda: "EmailMessage", name="@type")