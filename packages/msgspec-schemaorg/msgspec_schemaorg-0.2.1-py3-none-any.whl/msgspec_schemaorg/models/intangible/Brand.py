from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
from typing import Optional, Union, Dict, List, Any


class Brand(Intangible):
    """A brand is a name used by an organization or business person for labeling a product, product group, or similar."""
    type: str = field(default_factory=lambda: "Brand", name="@type")
    review: Union[List['Review'], 'Review', None] = None
    slogan: Union[List[str], str, None] = None
    logo: Union[List[Union['URL', 'ImageObject']], Union['URL', 'ImageObject'], None] = None
    aggregateRating: Union[List['AggregateRating'], 'AggregateRating', None] = None