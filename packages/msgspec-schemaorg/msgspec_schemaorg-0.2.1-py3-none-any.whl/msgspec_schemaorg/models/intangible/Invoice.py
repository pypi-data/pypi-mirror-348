from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.Order import Order
    from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
    from msgspec_schemaorg.enums.intangible.PaymentStatusType import PaymentStatusType
    from msgspec_schemaorg.enums.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class Invoice(Intangible):
    """A statement of the money due for goods or services; a bill."""
    type: str = field(default_factory=lambda: "Invoice", name="@type")
    paymentMethodId: Union[List[str], str, None] = None
    minimumPaymentDue: Union[List[Union['PriceSpecification', 'MonetaryAmount']], Union['PriceSpecification', 'MonetaryAmount'], None] = None
    scheduledPaymentDate: Union[List[date], date, None] = None
    confirmationNumber: Union[List[str], str, None] = None
    paymentMethod: Union[List[Union[str, 'PaymentMethod']], Union[str, 'PaymentMethod'], None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    totalPaymentDue: Union[List[Union['PriceSpecification', 'MonetaryAmount']], Union['PriceSpecification', 'MonetaryAmount'], None] = None
    paymentDueDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    accountId: Union[List[str], str, None] = None
    broker: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    category: Union[List[Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode']], Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode'], None] = None
    billingPeriod: Union[List['Duration'], 'Duration', None] = None
    customer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    paymentStatus: Union[List[Union[str, 'PaymentStatusType']], Union[str, 'PaymentStatusType'], None] = None
    referencesOrder: Union[List['Order'], 'Order', None] = None
    paymentDue: Union[List[datetime], datetime, None] = None