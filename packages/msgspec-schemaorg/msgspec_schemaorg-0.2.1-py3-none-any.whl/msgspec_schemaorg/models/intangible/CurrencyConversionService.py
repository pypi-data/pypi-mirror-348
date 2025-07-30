from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.FinancialProduct import FinancialProduct
from typing import Optional, Union, Dict, List, Any


class CurrencyConversionService(FinancialProduct):
    """A service to convert funds from one currency to another currency."""
    type: str = field(default_factory=lambda: "CurrencyConversionService", name="@type")