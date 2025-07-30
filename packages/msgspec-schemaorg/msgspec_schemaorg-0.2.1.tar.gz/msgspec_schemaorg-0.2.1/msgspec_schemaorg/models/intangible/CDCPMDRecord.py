from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from msgspec_schemaorg.utils import parse_iso8601
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class CDCPMDRecord(StructuredValue):
    """A CDCPMDRecord is a data structure representing a record in a CDC tabular data format
      used for hospital data reporting. See [documentation](/docs/cdc-covid.html) for details, and the linked CDC materials for authoritative
      definitions used as the source here.
      """
    type: str = field(default_factory=lambda: "CDCPMDRecord", name="@type")
    cvdCollectionDate: Union[List[Union[datetime, str]], Union[datetime, str], None] = None
    cvdNumVent: Union[List[int | float], int | float, None] = None
    datePosted: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    cvdNumVentUse: Union[List[int | float], int | float, None] = None
    cvdNumICUBeds: Union[List[int | float], int | float, None] = None
    cvdNumC19OverflowPats: Union[List[int | float], int | float, None] = None
    cvdNumBeds: Union[List[int | float], int | float, None] = None
    cvdFacilityCounty: Union[List[str], str, None] = None
    cvdFacilityId: Union[List[str], str, None] = None
    cvdNumC19OFMechVentPats: Union[List[int | float], int | float, None] = None
    cvdNumC19HospPats: Union[List[int | float], int | float, None] = None
    cvdNumBedsOcc: Union[List[int | float], int | float, None] = None
    cvdNumC19HOPats: Union[List[int | float], int | float, None] = None
    cvdNumICUBedsOcc: Union[List[int | float], int | float, None] = None
    cvdNumC19Died: Union[List[int | float], int | float, None] = None
    cvdNumC19MechVentPats: Union[List[int | float], int | float, None] = None
    cvdNumTotBeds: Union[List[int | float], int | float, None] = None