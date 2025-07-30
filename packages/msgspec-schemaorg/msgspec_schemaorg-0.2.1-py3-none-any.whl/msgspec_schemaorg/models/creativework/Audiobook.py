from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Book import Book
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Audiobook(Book):
    """An audiobook."""
    type: str = field(default_factory=lambda: "Audiobook", name="@type")
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    readBy: Union[List['Person'], 'Person', None] = None