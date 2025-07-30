from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.enums.intangible.MeasurementMethodEnum import MeasurementMethodEnum
    from msgspec_schemaorg.models.intangible.MeasurementTypeEnumeration import MeasurementTypeEnumeration
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import Optional, Union, Dict, List, Any


class PropertyValue(StructuredValue):
    """A property-value pair, e.g. representing a feature of a product or place. Use the 'name' property for the name of the property. If there is an additional human-readable version of the value, put that into the 'description' property.\\n\\n Always use specific schema.org properties when a) they exist and b) you can populate them. Using PropertyValue as a substitute will typically not trigger the same effect as using the original, specific property.
    """
    type: str = field(default_factory=lambda: "PropertyValue", name="@type")
    unitText: Union[List[str], str, None] = None
    minValue: Union[List[int | float], int | float, None] = None
    value: Union[List[Union[int | float, str, bool, 'StructuredValue']], Union[int | float, str, bool, 'StructuredValue'], None] = None
    measurementTechnique: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    propertyID: Union[List[Union['URL', str]], Union['URL', str], None] = None
    measurementMethod: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    maxValue: Union[List[int | float], int | float, None] = None
    valueReference: Union[List[Union[str, 'QualitativeValue', 'DefinedTerm', 'MeasurementTypeEnumeration', 'Enumeration', 'PropertyValue', 'StructuredValue', 'QuantitativeValue']], Union[str, 'QualitativeValue', 'DefinedTerm', 'MeasurementTypeEnumeration', 'Enumeration', 'PropertyValue', 'StructuredValue', 'QuantitativeValue'], None] = None
    unitCode: Union[List[Union['URL', str]], Union['URL', str], None] = None