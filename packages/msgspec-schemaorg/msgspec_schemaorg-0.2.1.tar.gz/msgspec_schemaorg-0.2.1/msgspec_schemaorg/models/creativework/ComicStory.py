from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class ComicStory(CreativeWork):
    """The term "story" is any indivisible, re-printable
    	unit of a comic, including the interior stories, covers, and backmatter. Most
    	comics have at least two stories: a cover (ComicCoverArt) and an interior story."""
    type: str = field(default_factory=lambda: "ComicStory", name="@type")
    artist: Union[List['Person'], 'Person', None] = None
    penciler: Union[List['Person'], 'Person', None] = None
    letterer: Union[List['Person'], 'Person', None] = None
    colorist: Union[List['Person'], 'Person', None] = None
    inker: Union[List['Person'], 'Person', None] = None