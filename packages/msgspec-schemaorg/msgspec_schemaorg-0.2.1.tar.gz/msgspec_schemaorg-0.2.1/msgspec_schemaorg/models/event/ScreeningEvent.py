from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Movie import Movie
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class ScreeningEvent(Event):
    """A screening of a movie or other video."""
    type: str = field(default_factory=lambda: "ScreeningEvent", name="@type")
    workPresented: Union[List['Movie'], 'Movie', None] = None
    subtitleLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    videoFormat: Union[List[str], str, None] = None