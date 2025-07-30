from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.PlanAction import PlanAction
from typing import Optional, Union, Dict, List, Any


class ScheduleAction(PlanAction):
    """Scheduling future actions, events, or tasks.\\n\\nRelated actions:\\n\\n* [[ReserveAction]]: Unlike ReserveAction, ScheduleAction allocates future actions (e.g. an event, a task, etc) towards a time slot / spatial allocation."""
    type: str = field(default_factory=lambda: "ScheduleAction", name="@type")