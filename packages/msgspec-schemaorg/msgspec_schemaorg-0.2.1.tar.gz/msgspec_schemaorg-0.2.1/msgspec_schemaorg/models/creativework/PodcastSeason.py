from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
from typing import Optional, Union, Dict, List, Any


class PodcastSeason(CreativeWorkSeason):
    """A single season of a podcast. Many podcasts do not break down into separate seasons. In that case, PodcastSeries should be used."""
    type: str = field(default_factory=lambda: "PodcastSeason", name="@type")