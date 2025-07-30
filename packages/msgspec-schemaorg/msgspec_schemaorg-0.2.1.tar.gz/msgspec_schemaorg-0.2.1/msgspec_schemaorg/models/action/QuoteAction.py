from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TradeAction import TradeAction
from typing import Optional, Union, Dict, List, Any


class QuoteAction(TradeAction):
    """An agent quotes/estimates/appraises an object/product/service with a price at a location/store."""
    type: str = field(default_factory=lambda: "QuoteAction", name="@type")