from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.QuantitativeValueDistribution import QuantitativeValueDistribution
from typing import Optional, Union, Dict, List, Any


class MonetaryAmountDistribution(QuantitativeValueDistribution):
    """A statistical distribution of monetary amounts."""
    type: str = field(default_factory=lambda: "MonetaryAmountDistribution", name="@type")
    currency: Union[List[str], str, None] = None