from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TradeAction import TradeAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.RealEstateAgent import RealEstateAgent
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class RentAction(TradeAction):
    """The act of giving money in return for temporary use, but not ownership, of an object such as a vehicle or property. For example, an agent rents a property from a landlord in exchange for a periodic payment."""
    type: str = field(default_factory=lambda: "RentAction", name="@type")
    realEstateAgent: Union[List['RealEstateAgent'], 'RealEstateAgent', None] = None
    landlord: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None