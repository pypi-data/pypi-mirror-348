from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class AudioObject(MediaObject):
    """An audio file."""
    type: str = field(default_factory=lambda: "AudioObject", name="@type")
    caption: Union[List[Union[str, 'MediaObject']], Union[str, 'MediaObject'], None] = None
    transcript: Union[List[str], str, None] = None
    embeddedTextCaption: Union[List[str], str, None] = None