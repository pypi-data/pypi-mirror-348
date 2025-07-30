from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ListItem import ListItem
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.HowToSupply import HowToSupply
    from msgspec_schemaorg.models.intangible.HowToTool import HowToTool
from typing import Optional, Union, Dict, List, Any


class HowToDirection(ListItem):
    """A direction indicating a single action to do in the instructions for how to achieve a result."""
    type: str = field(default_factory=lambda: "HowToDirection", name="@type")
    totalTime: Union[List['Duration'], 'Duration', None] = None
    beforeMedia: Union[List[Union['URL', 'MediaObject']], Union['URL', 'MediaObject'], None] = None
    tool: Union[List[Union[str, 'HowToTool']], Union[str, 'HowToTool'], None] = None
    performTime: Union[List['Duration'], 'Duration', None] = None
    supply: Union[List[Union[str, 'HowToSupply']], Union[str, 'HowToSupply'], None] = None
    duringMedia: Union[List[Union['URL', 'MediaObject']], Union['URL', 'MediaObject'], None] = None
    prepTime: Union[List['Duration'], 'Duration', None] = None
    afterMedia: Union[List[Union['URL', 'MediaObject']], Union['URL', 'MediaObject'], None] = None