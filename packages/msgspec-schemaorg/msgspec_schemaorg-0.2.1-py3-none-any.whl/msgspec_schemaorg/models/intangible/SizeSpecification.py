from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.GenderType import GenderType
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.SizeGroupEnumeration import SizeGroupEnumeration
    from msgspec_schemaorg.enums.intangible.SizeSystemEnumeration import SizeSystemEnumeration
from typing import Optional, Union, Dict, List, Any


class SizeSpecification(QualitativeValue):
    """Size related properties of a product, typically a size code ([[name]]) and optionally a [[sizeSystem]], [[sizeGroup]], and product measurements ([[hasMeasurement]]). In addition, the intended audience can be defined through [[suggestedAge]], [[suggestedGender]], and suggested body measurements ([[suggestedMeasurement]])."""
    type: str = field(default_factory=lambda: "SizeSpecification", name="@type")
    suggestedGender: Union[List[Union[str, 'GenderType']], Union[str, 'GenderType'], None] = None
    suggestedAge: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    sizeSystem: Union[List[Union[str, 'SizeSystemEnumeration']], Union[str, 'SizeSystemEnumeration'], None] = None
    suggestedMeasurement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    hasMeasurement: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    sizeGroup: Union[List[Union[str, 'SizeGroupEnumeration']], Union[str, 'SizeGroupEnumeration'], None] = None