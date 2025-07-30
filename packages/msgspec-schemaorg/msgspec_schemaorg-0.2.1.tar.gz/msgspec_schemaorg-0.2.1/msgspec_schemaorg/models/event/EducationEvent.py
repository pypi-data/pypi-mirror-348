from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
from typing import Optional, Union, Dict, List, Any


class EducationEvent(Event):
    """Event type: Education event."""
    type: str = field(default_factory=lambda: "EducationEvent", name="@type")
    assesses: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    teaches: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    educationalLevel: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None