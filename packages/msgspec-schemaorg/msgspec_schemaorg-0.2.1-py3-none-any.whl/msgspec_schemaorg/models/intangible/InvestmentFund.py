from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.InvestmentOrDeposit import InvestmentOrDeposit
from typing import Optional, Union, Dict, List, Any


class InvestmentFund(InvestmentOrDeposit):
    """A company or fund that gathers capital from a number of investors to create a pool of money that is then re-invested into stocks, bonds and other assets."""
    type: str = field(default_factory=lambda: "InvestmentFund", name="@type")