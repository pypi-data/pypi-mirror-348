from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CreateAction import CreateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class WriteAction(CreateAction):
    """The act of authoring written creative content."""
    type: str = field(default_factory=lambda: "WriteAction", name="@type")
    language: Union[List['Language'], 'Language', None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None