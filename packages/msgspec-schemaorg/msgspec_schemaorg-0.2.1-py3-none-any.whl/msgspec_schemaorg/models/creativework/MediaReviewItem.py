from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import Optional, Union, Dict, List, Any


class MediaReviewItem(CreativeWork):
    """Represents an item or group of closely related items treated as a unit for the sake of evaluation in a [[MediaReview]]. Authorship etc. apply to the items rather than to the curation/grouping or reviewing party."""
    type: str = field(default_factory=lambda: "MediaReviewItem", name="@type")
    mediaItemAppearance: Union[List['MediaObject'], 'MediaObject', None] = None