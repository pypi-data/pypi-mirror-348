from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.HyperTocEntry import HyperTocEntry
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class HyperToc(CreativeWork):
    """A HyperToc represents a hypertext table of contents for complex media objects, such as [[VideoObject]], [[AudioObject]]. Items in the table of contents are indicated using the [[tocEntry]] property, and typed [[HyperTocEntry]]. For cases where the same larger work is split into multiple files, [[associatedMedia]] can be used on individual [[HyperTocEntry]] items."""
    type: str = field(default_factory=lambda: "HyperToc", name="@type")
    associatedMedia: Union[List['MediaObject'], 'MediaObject', None] = None
    tocEntry: Union[List['HyperTocEntry'], 'HyperTocEntry', None] = None