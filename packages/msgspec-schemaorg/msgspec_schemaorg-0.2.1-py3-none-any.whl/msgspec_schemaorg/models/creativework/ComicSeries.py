from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Periodical import Periodical
from typing import Optional, Union, Dict, List, Any


class ComicSeries(Periodical):
    """A sequential publication of comic stories under a
    	unifying title, for example "The Amazing Spider-Man" or "Groo the
    	Wanderer"."""
    type: str = field(default_factory=lambda: "ComicSeries", name="@type")