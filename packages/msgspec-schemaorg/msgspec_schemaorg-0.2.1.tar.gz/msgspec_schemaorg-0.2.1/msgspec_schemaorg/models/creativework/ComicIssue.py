from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.PublicationIssue import PublicationIssue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class ComicIssue(PublicationIssue):
    """Individual comic issues are serially published as
    	part of a larger series. For the sake of consistency, even one-shot issues
    	belong to a series comprised of a single issue. All comic issues can be
    	uniquely identified by: the combination of the name and volume number of the
    	series to which the issue belongs; the issue number; and the variant
    	description of the issue (if any)."""
    type: str = field(default_factory=lambda: "ComicIssue", name="@type")
    artist: Union[List['Person'], 'Person', None] = None
    penciler: Union[List['Person'], 'Person', None] = None
    variantCover: Union[List[str], str, None] = None
    letterer: Union[List['Person'], 'Person', None] = None
    colorist: Union[List['Person'], 'Person', None] = None
    inker: Union[List['Person'], 'Person', None] = None