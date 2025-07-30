from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class LeaveAction(InteractAction):
    """An agent leaves an event / group with participants/friends at a location.\\n\\nRelated actions:\\n\\n* [[JoinAction]]: The antonym of LeaveAction.\\n* [[UnRegisterAction]]: Unlike UnRegisterAction, LeaveAction implies leaving a group/team of people rather than a service."""
    type: str = field(default_factory=lambda: "LeaveAction", name="@type")
    event: Union[List['Event'], 'Event', None] = None