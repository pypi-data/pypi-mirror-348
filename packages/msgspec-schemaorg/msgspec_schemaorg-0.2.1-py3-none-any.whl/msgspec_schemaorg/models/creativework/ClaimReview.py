from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Review import Review
from typing import Optional, Union, Dict, List, Any


class ClaimReview(Review):
    """A fact-checking review of claims made (or reported) in some creative work (referenced via itemReviewed)."""
    type: str = field(default_factory=lambda: "ClaimReview", name="@type")
    claimReviewed: Union[List[str], str, None] = None