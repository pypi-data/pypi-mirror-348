from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.HyperTocEntry import HyperTocEntry
from typing import Optional, Union, Dict, List, Any


class SeekToAction(Action):
    """This is the [[Action]] of navigating to a specific [[startOffset]] timestamp within a [[VideoObject]], typically represented with a URL template structure."""
    type: str = field(default_factory=lambda: "SeekToAction", name="@type")
    startOffset: Union[List[Union[int | float, 'HyperTocEntry']], Union[int | float, 'HyperTocEntry'], None] = None