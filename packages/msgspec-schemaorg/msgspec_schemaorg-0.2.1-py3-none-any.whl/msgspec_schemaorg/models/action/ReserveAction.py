from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.PlanAction import PlanAction
from typing import Optional, Union, Dict, List, Any


class ReserveAction(PlanAction):
    """Reserving a concrete object.\\n\\nRelated actions:\\n\\n* [[ScheduleAction]]: Unlike ScheduleAction, ReserveAction reserves concrete objects (e.g. a table, a hotel) towards a time slot / spatial allocation."""
    type: str = field(default_factory=lambda: "ReserveAction", name="@type")