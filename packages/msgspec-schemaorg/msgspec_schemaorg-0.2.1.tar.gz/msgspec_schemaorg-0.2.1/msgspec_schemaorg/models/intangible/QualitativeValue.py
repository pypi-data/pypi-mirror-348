from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.models.intangible.MeasurementTypeEnumeration import MeasurementTypeEnumeration
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import Optional, Union, Dict, List, Any


class QualitativeValue(Enumeration):
    """A predefined value for a product characteristic, e.g. the power cord plug type 'US' or the garment sizes 'S', 'M', 'L', and 'XL'."""
    type: str = field(default_factory=lambda: "QualitativeValue", name="@type")
    nonEqual: Union[List['QualitativeValue'], 'QualitativeValue', None] = None
    lesser: Union[List['QualitativeValue'], 'QualitativeValue', None] = None
    greaterOrEqual: Union[List['QualitativeValue'], 'QualitativeValue', None] = None
    equal: Union[List['QualitativeValue'], 'QualitativeValue', None] = None
    additionalProperty: Union[List['PropertyValue'], 'PropertyValue', None] = None
    greater: Union[List['QualitativeValue'], 'QualitativeValue', None] = None
    valueReference: Union[List[Union[str, 'QualitativeValue', 'DefinedTerm', 'MeasurementTypeEnumeration', 'Enumeration', 'PropertyValue', 'StructuredValue', 'QuantitativeValue']], Union[str, 'QualitativeValue', 'DefinedTerm', 'MeasurementTypeEnumeration', 'Enumeration', 'PropertyValue', 'StructuredValue', 'QuantitativeValue'], None] = None
    lesserOrEqual: Union[List['QualitativeValue'], 'QualitativeValue', None] = None