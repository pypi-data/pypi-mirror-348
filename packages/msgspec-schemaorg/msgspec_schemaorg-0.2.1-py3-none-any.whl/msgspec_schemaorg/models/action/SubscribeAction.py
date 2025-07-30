from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import Optional, Union, Dict, List, Any


class SubscribeAction(InteractAction):
    """The act of forming a personal connection with someone/something (object) unidirectionally/asymmetrically to get updates pushed to.\\n\\nRelated actions:\\n\\n* [[FollowAction]]: Unlike FollowAction, SubscribeAction implies that the subscriber acts as a passive agent being constantly/actively pushed for updates.\\n* [[RegisterAction]]: Unlike RegisterAction, SubscribeAction implies that the agent is interested in continuing receiving updates from the object.\\n* [[JoinAction]]: Unlike JoinAction, SubscribeAction implies that the agent is interested in continuing receiving updates from the object."""
    type: str = field(default_factory=lambda: "SubscribeAction", name="@type")