from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Poster(CreativeWork):
    """A large, usually printed placard, bill, or announcement, often illustrated, that is posted to advertise or publicize something."""
    type: str = field(default_factory=lambda: "Poster", name="@type")