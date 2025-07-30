from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from msgspec_schemaorg.utils import URL
from typing import Optional, Union, Dict, List, Any


class FinancialService(LocalBusiness):
    """Financial services business."""
    type: str = field(default_factory=lambda: "FinancialService", name="@type")
    feesAndCommissionsSpecification: Union[List[Union['URL', str]], Union['URL', str], None] = None