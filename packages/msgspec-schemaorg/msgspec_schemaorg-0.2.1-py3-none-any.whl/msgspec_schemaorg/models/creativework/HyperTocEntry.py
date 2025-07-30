from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.HyperTocEntry import HyperTocEntry
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class HyperTocEntry(CreativeWork):
    """A HyperToEntry is an item within a [[HyperToc]], which represents a hypertext table of contents for complex media objects, such as [[VideoObject]], [[AudioObject]]. The media object itself is indicated using [[associatedMedia]]. Each section of interest within that content can be described with a [[HyperTocEntry]], with associated [[startOffset]] and [[endOffset]]. When several entries are all from the same file, [[associatedMedia]] is used on the overarching [[HyperTocEntry]]; if the content has been split into multiple files, they can be referenced using [[associatedMedia]] on each [[HyperTocEntry]]."""
    type: str = field(default_factory=lambda: "HyperTocEntry", name="@type")
    utterances: Union[List[str], str, None] = None
    tocContinuation: Union[List['HyperTocEntry'], 'HyperTocEntry', None] = None
    associatedMedia: Union[List['MediaObject'], 'MediaObject', None] = None