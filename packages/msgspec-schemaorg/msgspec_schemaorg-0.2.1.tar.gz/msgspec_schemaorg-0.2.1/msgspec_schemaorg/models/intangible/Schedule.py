from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DayOfWeek import DayOfWeek
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class Schedule(Intangible):
    """A schedule defines a repeating time period used to describe a regularly occurring [[Event]]. At a minimum a schedule will specify [[repeatFrequency]] which describes the interval between occurrences of the event. Additional information can be provided to specify the schedule more precisely.
      This includes identifying the day(s) of the week or month when the recurring event will take place, in addition to its start and end time. Schedules may also
      have start and end dates to indicate when they are active, e.g. to define a limited calendar of events."""
    type: str = field(default_factory=lambda: "Schedule", name="@type")
    repeatCount: Union[List[int], int, None] = None
    byMonthDay: Union[List[int], int, None] = None
    startTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    scheduleTimezone: Union[List[str], str, None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    endTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    repeatFrequency: Union[List[Union[str, 'Duration']], Union[str, 'Duration'], None] = None
    byMonthWeek: Union[List[int], int, None] = None
    byDay: Union[List[Union[str, 'DayOfWeek']], Union[str, 'DayOfWeek'], None] = None
    byMonth: Union[List[int], int, None] = None
    exceptDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None