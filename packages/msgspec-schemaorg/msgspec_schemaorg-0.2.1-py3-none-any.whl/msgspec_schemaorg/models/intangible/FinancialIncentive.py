from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.enums.intangible.IncentiveQualifiedExpenseType import IncentiveQualifiedExpenseType
    from msgspec_schemaorg.enums.intangible.IncentiveStatus import IncentiveStatus
    from msgspec_schemaorg.enums.intangible.IncentiveType import IncentiveType
    from msgspec_schemaorg.models.intangible.LoanOrCredit import LoanOrCredit
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.enums.intangible.PurchaseType import PurchaseType
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.UnitPriceSpecification import UnitPriceSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class FinancialIncentive(Intangible):
    """<p>Represents financial incentives for goods/services offered by an organization (or individual).</p>

<p>Typically contains the [[name]] of the incentive, the [[incentivizedItem]], the [[incentiveAmount]], the [[incentiveStatus]], [[incentiveType]], the [[provider]] of the incentive, and [[eligibleWithSupplier]].</p>

<p>Optionally contains criteria on whether the incentive is limited based on [[purchaseType]], [[purchasePriceLimit]], [[incomeLimit]], and the [[qualifiedExpense]].
    """
    type: str = field(default_factory=lambda: "FinancialIncentive", name="@type")
    incentivizedItem: Union[List[Union['Product', 'DefinedTerm']], Union['Product', 'DefinedTerm'], None] = None
    purchasePriceLimit: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    incentiveStatus: Union[List['IncentiveStatus'], 'IncentiveStatus', None] = None
    purchaseType: Union[List['PurchaseType'], 'PurchaseType', None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    areaServed: Union[List[Union[str, 'AdministrativeArea', 'Place', 'GeoShape']], Union[str, 'AdministrativeArea', 'Place', 'GeoShape'], None] = None
    eligibleWithSupplier: Union[List['Organization'], 'Organization', None] = None
    qualifiedExpense: Union[List['IncentiveQualifiedExpenseType'], 'IncentiveQualifiedExpenseType', None] = None
    incentiveAmount: Union[List[Union['QuantitativeValue', 'UnitPriceSpecification', 'LoanOrCredit']], Union['QuantitativeValue', 'UnitPriceSpecification', 'LoanOrCredit'], None] = None
    incentiveType: Union[List['IncentiveType'], 'IncentiveType', None] = None
    incomeLimit: Union[List[Union[str, 'MonetaryAmount']], Union[str, 'MonetaryAmount'], None] = None
    publisher: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    validThrough: Union[List[Union[datetime, date]], Union[datetime, date], None] = None