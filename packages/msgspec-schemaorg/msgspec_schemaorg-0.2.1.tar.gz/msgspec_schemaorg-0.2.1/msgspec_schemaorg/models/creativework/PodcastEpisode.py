from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Episode import Episode
from typing import Optional, Union, Dict, List, Any


class PodcastEpisode(Episode):
    """A single episode of a podcast series."""
    type: str = field(default_factory=lambda: "PodcastEpisode", name="@type")