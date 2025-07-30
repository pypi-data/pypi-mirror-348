from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TradeAction import TradeAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
from typing import Optional, Union, Dict, List, Any


class OrderAction(TradeAction):
    """An agent orders an object/product/service to be delivered/sent."""
    type: str = field(default_factory=lambda: "OrderAction", name="@type")
    deliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None