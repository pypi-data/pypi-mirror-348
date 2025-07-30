from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
from typing import Optional, Union, Dict, List, Any


class EmployerAggregateRating(AggregateRating):
    """An aggregate rating of an Organization related to its role as an employer."""
    type: str = field(default_factory=lambda: "EmployerAggregateRating", name="@type")