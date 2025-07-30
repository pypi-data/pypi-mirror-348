from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import Optional, Union, Dict, List, Any


class BefriendAction(InteractAction):
    """The act of forming a personal connection with someone (object) mutually/bidirectionally/symmetrically.\\n\\nRelated actions:\\n\\n* [[FollowAction]]: Unlike FollowAction, BefriendAction implies that the connection is reciprocal."""
    type: str = field(default_factory=lambda: "BefriendAction", name="@type")