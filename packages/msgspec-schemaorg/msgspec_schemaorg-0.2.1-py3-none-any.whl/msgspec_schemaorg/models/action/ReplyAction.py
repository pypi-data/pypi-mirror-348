from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Comment import Comment
from typing import Optional, Union, Dict, List, Any


class ReplyAction(CommunicateAction):
    """The act of responding to a question/message asked/sent by the object. Related to [[AskAction]].\\n\\nRelated actions:\\n\\n* [[AskAction]]: Appears generally as an origin of a ReplyAction."""
    type: str = field(default_factory=lambda: "ReplyAction", name="@type")
    resultComment: Union[List['Comment'], 'Comment', None] = None