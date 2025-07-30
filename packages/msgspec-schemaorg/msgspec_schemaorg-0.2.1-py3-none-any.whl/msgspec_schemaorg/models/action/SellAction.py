from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TradeAction import TradeAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.WarrantyPromise import WarrantyPromise
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class SellAction(TradeAction):
    """The act of taking money from a buyer in exchange for goods or services rendered. An agent sells an object, product, or service to a buyer for a price. Reciprocal of BuyAction."""
    type: str = field(default_factory=lambda: "SellAction", name="@type")
    buyer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    warrantyPromise: Union[List['WarrantyPromise'], 'WarrantyPromise', None] = None