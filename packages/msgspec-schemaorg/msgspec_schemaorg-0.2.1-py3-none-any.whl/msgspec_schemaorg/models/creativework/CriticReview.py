from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Review import Review
from typing import Optional, Union, Dict, List, Any


class CriticReview(Review):
    """A [[CriticReview]] is a more specialized form of Review written or published by a source that is recognized for its reviewing activities. These can include online columns, travel and food guides, TV and radio shows, blogs and other independent Web sites. [[CriticReview]]s are typically more in-depth and professionally written. For simpler, casually written user/visitor/viewer/customer reviews, it is more appropriate to use the [[UserReview]] type. Review aggregator sites such as Metacritic already separate out the site's user reviews from selected critic reviews that originate from third-party sources."""
    type: str = field(default_factory=lambda: "CriticReview", name="@type")