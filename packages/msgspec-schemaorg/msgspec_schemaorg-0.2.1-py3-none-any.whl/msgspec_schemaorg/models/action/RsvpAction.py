from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InformAction import InformAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.enums.intangible.RsvpResponseType import RsvpResponseType
from typing import Optional, Union, Dict, List, Any


class RsvpAction(InformAction):
    """The act of notifying an event organizer as to whether you expect to attend the event."""
    type: str = field(default_factory=lambda: "RsvpAction", name="@type")
    additionalNumberOfGuests: Union[List[int | float], int | float, None] = None
    rsvpResponse: Union[List['RsvpResponseType'], 'RsvpResponseType', None] = None
    comment: Union[List['Comment'], 'Comment', None] = None