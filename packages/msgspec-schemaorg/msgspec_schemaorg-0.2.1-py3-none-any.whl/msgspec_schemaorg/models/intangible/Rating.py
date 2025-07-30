from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Rating(Intangible):
    """A rating is an evaluation on a numeric scale, such as 1 to 5 stars."""
    type: str = field(default_factory=lambda: "Rating", name="@type")
    worstRating: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    author: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    ratingValue: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    bestRating: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    ratingExplanation: Union[List[str], str, None] = None
    reviewAspect: Union[List[str], str, None] = None