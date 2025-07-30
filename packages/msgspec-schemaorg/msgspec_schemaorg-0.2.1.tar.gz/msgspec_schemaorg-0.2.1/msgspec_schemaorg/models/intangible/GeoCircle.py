from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.GeoCoordinates import GeoCoordinates
from typing import Optional, Union, Dict, List, Any


class GeoCircle(GeoShape):
    """A GeoCircle is a GeoShape representing a circular geographic area. As it is a GeoShape
          it provides the simple textual property 'circle', but also allows the combination of postalCode alongside geoRadius.
          The center of the circle can be indicated via the 'geoMidpoint' property, or more approximately using 'address', 'postalCode'.
       """
    type: str = field(default_factory=lambda: "GeoCircle", name="@type")
    geoRadius: Union[List[Union[int | float, str, 'Distance']], Union[int | float, str, 'Distance'], None] = None
    geoMidpoint: Union[List['GeoCoordinates'], 'GeoCoordinates', None] = None