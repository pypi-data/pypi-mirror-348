from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Review import Review
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.creativework.WebPage import WebPage
    from msgspec_schemaorg.enums.intangible.MediaManipulationRatingEnumeration import MediaManipulationRatingEnumeration
from typing import Optional, Union, Dict, List, Any


class MediaReview(Review):
    """A [[MediaReview]] is a more specialized form of Review dedicated to the evaluation of media content online, typically in the context of fact-checking and misinformation.
    For more general reviews of media in the broader sense, use [[UserReview]], [[CriticReview]] or other [[Review]] types. This definition is
    a work in progress. While the [[MediaManipulationRatingEnumeration]] list reflects significant community review amongst fact-checkers and others working
    to combat misinformation, the specific structures for representing media objects, their versions and publication context, are still evolving. Similarly, best practices for the relationship between [[MediaReview]] and [[ClaimReview]] markup have not yet been finalized."""
    type: str = field(default_factory=lambda: "MediaReview", name="@type")
    originalMediaLink: Union[List[Union['URL', 'MediaObject', 'WebPage']], Union['URL', 'MediaObject', 'WebPage'], None] = None
    originalMediaContextDescription: Union[List[str], str, None] = None
    mediaAuthenticityCategory: Union[List['MediaManipulationRatingEnumeration'], 'MediaManipulationRatingEnumeration', None] = None