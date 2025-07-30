from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.enums.intangible.MerchantReturnEnumeration import MerchantReturnEnumeration
    from msgspec_schemaorg.models.intangible.MerchantReturnPolicySeasonalOverride import MerchantReturnPolicySeasonalOverride
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.enums.intangible.OfferItemCondition import OfferItemCondition
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.enums.intangible.RefundTypeEnumeration import RefundTypeEnumeration
    from msgspec_schemaorg.enums.intangible.ReturnFeesEnumeration import ReturnFeesEnumeration
    from msgspec_schemaorg.enums.intangible.ReturnLabelSourceEnumeration import ReturnLabelSourceEnumeration
    from msgspec_schemaorg.enums.intangible.ReturnMethodEnumeration import ReturnMethodEnumeration
    from msgspec_schemaorg.models.place.Country import Country
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class MerchantReturnPolicy(Intangible):
    """A MerchantReturnPolicy provides information about product return policies associated with an [[Organization]], [[Product]], or [[Offer]]."""
    type: str = field(default_factory=lambda: "MerchantReturnPolicy", name="@type")
    itemDefectReturnShippingFeesAmount: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    applicableCountry: Union[List[Union[str, 'Country']], Union[str, 'Country'], None] = None
    returnPolicyCountry: Union[List[Union[str, 'Country']], Union[str, 'Country'], None] = None
    returnPolicySeasonalOverride: Union[List['MerchantReturnPolicySeasonalOverride'], 'MerchantReturnPolicySeasonalOverride', None] = None
    additionalProperty: Union[List['PropertyValue'], 'PropertyValue', None] = None
    returnPolicyCategory: Union[List['MerchantReturnEnumeration'], 'MerchantReturnEnumeration', None] = None
    merchantReturnLink: Union[List['URL'], 'URL', None] = None
    customerRemorseReturnShippingFeesAmount: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None
    returnMethod: Union[List['ReturnMethodEnumeration'], 'ReturnMethodEnumeration', None] = None
    customerRemorseReturnLabelSource: Union[List['ReturnLabelSourceEnumeration'], 'ReturnLabelSourceEnumeration', None] = None
    returnFees: Union[List['ReturnFeesEnumeration'], 'ReturnFeesEnumeration', None] = None
    itemDefectReturnLabelSource: Union[List['ReturnLabelSourceEnumeration'], 'ReturnLabelSourceEnumeration', None] = None
    inStoreReturnsOffered: Union[List[bool], bool, None] = None
    customerRemorseReturnFees: Union[List['ReturnFeesEnumeration'], 'ReturnFeesEnumeration', None] = None
    merchantReturnDays: Union[List[Union[int, datetime, date]], Union[int, datetime, date], None] = None
    returnLabelSource: Union[List['ReturnLabelSourceEnumeration'], 'ReturnLabelSourceEnumeration', None] = None
    restockingFee: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None
    refundType: Union[List['RefundTypeEnumeration'], 'RefundTypeEnumeration', None] = None
    itemDefectReturnFees: Union[List['ReturnFeesEnumeration'], 'ReturnFeesEnumeration', None] = None
    validForMemberTier: Union[List['MemberProgramTier'], 'MemberProgramTier', None] = None
    itemCondition: Union[List['OfferItemCondition'], 'OfferItemCondition', None] = None
    returnShippingFeesAmount: Union[List['MonetaryAmount'], 'MonetaryAmount', None] = None