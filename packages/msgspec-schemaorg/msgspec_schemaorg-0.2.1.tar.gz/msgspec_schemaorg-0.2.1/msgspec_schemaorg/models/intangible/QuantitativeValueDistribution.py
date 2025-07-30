from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class QuantitativeValueDistribution(StructuredValue):
    """A statistical distribution of values."""
    type: str = field(default_factory=lambda: "QuantitativeValueDistribution", name="@type")
    percentile25: Union[List[int | float], int | float, None] = None
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    percentile10: Union[List[int | float], int | float, None] = None
    median: Union[List[int | float], int | float, None] = None
    percentile75: Union[List[int | float], int | float, None] = None
    percentile90: Union[List[int | float], int | float, None] = None