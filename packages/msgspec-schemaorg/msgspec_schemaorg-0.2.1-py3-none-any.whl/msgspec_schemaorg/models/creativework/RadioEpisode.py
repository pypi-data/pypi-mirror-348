from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Episode import Episode
from typing import Optional, Union, Dict, List, Any


class RadioEpisode(Episode):
    """A radio episode which can be part of a series or season."""
    type: str = field(default_factory=lambda: "RadioEpisode", name="@type")