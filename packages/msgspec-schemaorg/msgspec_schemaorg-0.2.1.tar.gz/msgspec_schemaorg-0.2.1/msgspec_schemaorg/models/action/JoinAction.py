from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class JoinAction(InteractAction):
    """An agent joins an event/group with participants/friends at a location.\\n\\nRelated actions:\\n\\n* [[RegisterAction]]: Unlike RegisterAction, JoinAction refers to joining a group/team of people.\\n* [[SubscribeAction]]: Unlike SubscribeAction, JoinAction does not imply that you'll be receiving updates.\\n* [[FollowAction]]: Unlike FollowAction, JoinAction does not imply that you'll be polling for updates."""
    type: str = field(default_factory=lambda: "JoinAction", name="@type")
    event: Union[List['Event'], 'Event', None] = None