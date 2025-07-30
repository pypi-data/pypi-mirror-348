from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MerchantReturnEnumeration import MerchantReturnEnumeration
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.enums.intangible.RefundTypeEnumeration import RefundTypeEnumeration
    from msgspec_schemaorg.enums.intangible.ReturnFeesEnumeration import ReturnFeesEnumeration
    from msgspec_schemaorg.enums.intangible.ReturnMethodEnumeration import ReturnMethodEnumeration
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class MerchantReturnPolicySeasonalOverride(Intangible):
    """A seasonal override of a return policy, for example used for holidays."""
    type: str = field(default_factory=lambda: "MerchantReturnPolicySeasonalOverride", name="@type")
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    returnPolicyCategory: Union[List['MerchantReturnEnumeration'], 'MerchantReturnEnumeration', None] = None
    returnMethod: Union[List['ReturnMethodEnumeration'], 'ReturnMethodEnumeration', None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    returnFees: Union[List['ReturnFeesEnumeration'], 'ReturnFeesEnumeration', None] = None
    merchantReturnDays: Union[List[Union[int, datetime, date]], Union[int, datetime, date], None] = None
    restockingFee: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None
    refundType: Union[List['RefundTypeEnumeration'], 'RefundTypeEnumeration', None] = None
    returnShippingFeesAmount: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None