from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.FinancialService import FinancialService
from typing import Optional, Union, Dict, List, Any


class AutomatedTeller(FinancialService):
    """ATM/cash machine."""
    type: str = field(default_factory=lambda: "AutomatedTeller", name="@type")