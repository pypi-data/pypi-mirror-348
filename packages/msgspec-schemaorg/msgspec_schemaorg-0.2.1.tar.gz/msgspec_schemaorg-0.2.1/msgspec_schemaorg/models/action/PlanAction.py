from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.OrganizeAction import OrganizeAction
from msgspec_schemaorg.utils import parse_iso8601
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class PlanAction(OrganizeAction):
    """The act of planning the execution of an event/task/action/reservation/plan to a future date."""
    type: str = field(default_factory=lambda: "PlanAction", name="@type")
    scheduledTime: Union[List[Union[datetime, date]], Union[datetime, date], None] = None