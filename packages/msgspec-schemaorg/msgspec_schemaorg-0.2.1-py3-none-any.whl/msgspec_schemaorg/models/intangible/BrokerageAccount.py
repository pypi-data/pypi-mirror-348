from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.InvestmentOrDeposit import InvestmentOrDeposit
from typing import Optional, Union, Dict, List, Any


class BrokerageAccount(InvestmentOrDeposit):
    """An account that allows an investor to deposit funds and place investment orders with a licensed broker or brokerage firm."""
    type: str = field(default_factory=lambda: "BrokerageAccount", name="@type")