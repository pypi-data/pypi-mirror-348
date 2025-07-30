from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Question import Question
from typing import Optional, Union, Dict, List, Any


class AskAction(CommunicateAction):
    """The act of posing a question / favor to someone.\\n\\nRelated actions:\\n\\n* [[ReplyAction]]: Appears generally as a response to AskAction."""
    type: str = field(default_factory=lambda: "AskAction", name="@type")
    question: Union[List['Question'], 'Question', None] = None