from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Grant import Grant
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MonetaryGrant(Grant):
    """A monetary grant."""
    type: str = field(default_factory=lambda: "MonetaryGrant", name="@type")
    amount: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None
    funder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None