from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
from typing import Optional, Union, Dict, List, Any


class ImageObjectSnapshot(ImageObject):
    """A specific and exact (byte-for-byte) version of an [[ImageObject]]. Two byte-for-byte identical files, for the purposes of this type, considered identical. If they have different embedded metadata (e.g. XMP, EXIF) the files will differ. Different external facts about the files, e.g. creator or dateCreated that aren't represented in their actual content, do not affect this notion of identity."""
    type: str = field(default_factory=lambda: "ImageObjectSnapshot", name="@type")