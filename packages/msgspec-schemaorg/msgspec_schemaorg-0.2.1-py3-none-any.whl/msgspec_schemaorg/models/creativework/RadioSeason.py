from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
from typing import Optional, Union, Dict, List, Any


class RadioSeason(CreativeWorkSeason):
    """Season dedicated to radio broadcast and associated online delivery."""
    type: str = field(default_factory=lambda: "RadioSeason", name="@type")