from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import Optional, Union, Dict, List, Any


class TradeAction(Action):
    """The act of participating in an exchange of goods and services for monetary compensation. An agent trades an object, product or service with a participant in exchange for a one time or periodic payment."""
    type: str = field(default_factory=lambda: "TradeAction", name="@type")
    priceCurrency: Union[List[str], str, None] = None
    priceSpecification: Union[List['PriceSpecification'], 'PriceSpecification', None] = None
    price: Union[List[Union[int | float, str]], Union[int | float, str], None] = None