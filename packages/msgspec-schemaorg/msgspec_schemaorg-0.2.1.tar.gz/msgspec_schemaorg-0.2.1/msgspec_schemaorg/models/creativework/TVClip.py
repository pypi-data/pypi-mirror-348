from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Clip import Clip
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.TVSeries import TVSeries
from typing import Optional, Union, Dict, List, Any


class TVClip(Clip):
    """A short TV program or a segment/part of a TV program."""
    type: str = field(default_factory=lambda: "TVClip", name="@type")
    partOfTVSeries: Union[List['TVSeries'], 'TVSeries', None] = None