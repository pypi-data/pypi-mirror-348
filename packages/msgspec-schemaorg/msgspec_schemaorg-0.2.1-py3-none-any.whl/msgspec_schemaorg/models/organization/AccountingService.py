from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.FinancialService import FinancialService
from typing import Optional, Union, Dict, List, Any


class AccountingService(FinancialService):
    """Accountancy business.\\n\\nAs a [[LocalBusiness]] it can be described as a [[provider]] of one or more [[Service]]\\(s).
      """
    type: str = field(default_factory=lambda: "AccountingService", name="@type")