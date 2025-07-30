from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.ComicStory import ComicStory
from typing import Optional, Union, Dict, List, Any


class ComicCoverArt(ComicStory):
    """The artwork on the cover of a comic."""
    type: str = field(default_factory=lambda: "ComicCoverArt", name="@type")