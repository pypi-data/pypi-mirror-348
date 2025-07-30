from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Comment import Comment
from typing import Optional, Union, Dict, List, Any


class CommentAction(CommunicateAction):
    """The act of generating a comment about a subject."""
    type: str = field(default_factory=lambda: "CommentAction", name="@type")
    resultComment: Union[List['Comment'], 'Comment', None] = None