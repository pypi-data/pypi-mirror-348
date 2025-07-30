from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TradeAction import TradeAction
from typing import Optional, Union, Dict, List, Any


class PreOrderAction(TradeAction):
    """An agent orders a (not yet released) object/product/service to be delivered/sent."""
    type: str = field(default_factory=lambda: "PreOrderAction", name="@type")