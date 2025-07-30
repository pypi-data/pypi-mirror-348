from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.Event import Event
from typing import Optional, Union, Dict, List, Any


class InviteAction(CommunicateAction):
    """The act of asking someone to attend an event. Reciprocal of RsvpAction."""
    type: str = field(default_factory=lambda: "InviteAction", name="@type")
    event: Union[List['Event'], 'Event', None] = None