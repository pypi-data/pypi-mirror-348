from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Periodical import Periodical
from typing import Optional, Union, Dict, List, Any


class Newspaper(Periodical):
    """A publication containing information about varied topics that are pertinent to general information, a geographic area, or a specific subject matter (i.e. business, culture, education). Often published daily."""
    type: str = field(default_factory=lambda: "Newspaper", name="@type")