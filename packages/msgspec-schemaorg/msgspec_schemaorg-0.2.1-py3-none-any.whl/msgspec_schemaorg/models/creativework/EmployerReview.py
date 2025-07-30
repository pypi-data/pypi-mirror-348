from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Review import Review
from typing import Optional, Union, Dict, List, Any


class EmployerReview(Review):
    """An [[EmployerReview]] is a review of an [[Organization]] regarding its role as an employer, written by a current or former employee of that organization."""
    type: str = field(default_factory=lambda: "EmployerReview", name="@type")