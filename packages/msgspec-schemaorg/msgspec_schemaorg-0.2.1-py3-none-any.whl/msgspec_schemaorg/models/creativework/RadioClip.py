from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Clip import Clip
from typing import Optional, Union, Dict, List, Any


class RadioClip(Clip):
    """A short radio program or a segment/part of a radio program."""
    type: str = field(default_factory=lambda: "RadioClip", name="@type")