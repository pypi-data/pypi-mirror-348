from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
from typing import Optional, Union, Dict, List, Any


class ImageObject(MediaObject):
    """An image file."""
    type: str = field(default_factory=lambda: "ImageObject", name="@type")
    caption: Union[List[Union[str, 'MediaObject']], Union[str, 'MediaObject'], None] = None
    representativeOfPage: Union[List[bool], bool, None] = None
    embeddedTextCaption: Union[List[str], str, None] = None
    exifData: Union[List[Union[str, 'PropertyValue']], Union[str, 'PropertyValue'], None] = None