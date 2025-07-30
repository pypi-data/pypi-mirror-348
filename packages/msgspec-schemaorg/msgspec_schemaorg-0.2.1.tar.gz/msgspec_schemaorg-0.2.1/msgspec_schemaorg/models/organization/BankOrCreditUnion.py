from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.FinancialService import FinancialService
from typing import Optional, Union, Dict, List, Any


class BankOrCreditUnion(FinancialService):
    """Bank or credit union."""
    type: str = field(default_factory=lambda: "BankOrCreditUnion", name="@type")