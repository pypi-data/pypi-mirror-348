from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Review import Review
from typing import Optional, Union, Dict, List, Any


class UserReview(Review):
    """A review created by an end-user (e.g. consumer, purchaser, attendee etc.), in contrast with [[CriticReview]]."""
    type: str = field(default_factory=lambda: "UserReview", name="@type")