from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import Optional, Union, Dict, List, Any


class RegisterAction(InteractAction):
    """The act of registering to be a user of a service, product or web page.\\n\\nRelated actions:\\n\\n* [[JoinAction]]: Unlike JoinAction, RegisterAction implies you are registering to be a user of a service, *not* a group/team of people.\\n* [[FollowAction]]: Unlike FollowAction, RegisterAction doesn't imply that the agent is expecting to poll for updates from the object.\\n* [[SubscribeAction]]: Unlike SubscribeAction, RegisterAction doesn't imply that the agent is expecting updates from the object."""
    type: str = field(default_factory=lambda: "RegisterAction", name="@type")