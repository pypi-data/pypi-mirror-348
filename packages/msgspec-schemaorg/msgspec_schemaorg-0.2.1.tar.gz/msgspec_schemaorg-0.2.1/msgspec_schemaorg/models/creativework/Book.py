from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.BookFormatType import BookFormatType
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Book(CreativeWork):
    """A book."""
    type: str = field(default_factory=lambda: "Book", name="@type")
    bookEdition: Union[List[str], str, None] = None
    isbn: Union[List[str], str, None] = None
    bookFormat: Union[List['BookFormatType'], 'BookFormatType', None] = None
    numberOfPages: Union[List[int], int, None] = None
    abridged: Union[List[bool], bool, None] = None
    illustrator: Union[List['Person'], 'Person', None] = None