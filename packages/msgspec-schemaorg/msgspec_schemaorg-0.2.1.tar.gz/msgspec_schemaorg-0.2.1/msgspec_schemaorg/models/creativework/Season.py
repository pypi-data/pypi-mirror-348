from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Season(CreativeWork):
    """A media season, e.g. TV, radio, video game etc."""
    type: str = field(default_factory=lambda: "Season", name="@type")