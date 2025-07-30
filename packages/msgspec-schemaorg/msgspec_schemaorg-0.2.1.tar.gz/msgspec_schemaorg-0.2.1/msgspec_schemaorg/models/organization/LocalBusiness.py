from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class LocalBusiness(Organization):
    """A particular physical business or branch of an organization. Examples of LocalBusiness include a restaurant, a particular branch of a restaurant chain, a branch of a bank, a medical practice, a club, a bowling alley, etc."""
    type: str = field(default_factory=lambda: "LocalBusiness", name="@type")
    currenciesAccepted: Union[List[str], str, None] = None
    openingHours: Union[List[str], str, None] = None
    priceRange: Union[List[str], str, None] = None
    paymentAccepted: Union[List[str], str, None] = None
    branchOf: Union[List['Organization'], 'Organization', None] = None