from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TradeAction import TradeAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.WarrantyPromise import WarrantyPromise
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class BuyAction(TradeAction):
    """The act of giving money to a seller in exchange for goods or services rendered. An agent buys an object, product, or service from a seller for a price. Reciprocal of SellAction."""
    type: str = field(default_factory=lambda: "BuyAction", name="@type")
    seller: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    warrantyPromise: Union[List['WarrantyPromise'], 'WarrantyPromise', None] = None
    vendor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None