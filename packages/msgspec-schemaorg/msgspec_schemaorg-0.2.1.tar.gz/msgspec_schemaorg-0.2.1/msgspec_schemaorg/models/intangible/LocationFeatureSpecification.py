from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.OpeningHoursSpecification import OpeningHoursSpecification
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class LocationFeatureSpecification(PropertyValue):
    """Specifies a location feature by providing a structured value representing a feature of an accommodation as a property-value pair of varying degrees of formality."""
    type: str = field(default_factory=lambda: "LocationFeatureSpecification", name="@type")
    validFrom: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    hoursAvailable: Union[List['OpeningHoursSpecification'], 'OpeningHoursSpecification', None] = None
    validThrough: Union[List[Union[datetime, date]], Union[datetime, date], None] = None