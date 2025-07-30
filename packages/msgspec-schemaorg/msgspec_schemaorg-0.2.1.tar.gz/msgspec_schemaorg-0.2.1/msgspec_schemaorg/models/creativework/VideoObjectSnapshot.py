from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
from typing import Optional, Union, Dict, List, Any


class VideoObjectSnapshot(VideoObject):
    """A specific and exact (byte-for-byte) version of a [[VideoObject]]. Two byte-for-byte identical files, for the purposes of this type, considered identical. If they have different embedded metadata the files will differ. Different external facts about the files, e.g. creator or dateCreated that aren't represented in their actual content, do not affect this notion of identity."""
    type: str = field(default_factory=lambda: "VideoObjectSnapshot", name="@type")