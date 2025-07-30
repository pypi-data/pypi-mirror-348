from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.OrganizationRole import OrganizationRole
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
from typing import Optional, Union, Dict, List, Any


class EmployeeRole(OrganizationRole):
    """A subclass of OrganizationRole used to describe employee relationships."""
    type: str = field(default_factory=lambda: "EmployeeRole", name="@type")
    baseSalary: Union[List[Union[int | float, 'PriceSpecification', 'MonetaryAmount']], Union[int | float, 'PriceSpecification', 'MonetaryAmount'], None] = None
    salaryCurrency: Union[List[str], str, None] = None