from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.creativework.WebContent import WebContent
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.ListItem import ListItem
    from msgspec_schemaorg.models.intangible.Rating import Rating
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class Review(CreativeWork):
    """A review of an item - for example, of a restaurant, movie, or store."""
    type: str = field(default_factory=lambda: "Review", name="@type")
    associatedMediaReview: Union[List['Review'], 'Review', None] = None
    itemReviewed: Union[List['Thing'], 'Thing', None] = None
    reviewRating: Union[List['Rating'], 'Rating', None] = None
    reviewBody: Union[List[str], str, None] = None
    associatedClaimReview: Union[List['Review'], 'Review', None] = None
    negativeNotes: Union[List[Union[str, 'ListItem', 'WebContent', 'ItemList']], Union[str, 'ListItem', 'WebContent', 'ItemList'], None] = None
    associatedReview: Union[List['Review'], 'Review', None] = None
    reviewAspect: Union[List[str], str, None] = None
    positiveNotes: Union[List[Union[str, 'ListItem', 'ItemList', 'WebContent']], Union[str, 'ListItem', 'ItemList', 'WebContent'], None] = None