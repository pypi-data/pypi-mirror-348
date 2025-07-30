from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import Optional, Union, Dict, List, Any


class CheckOutAction(CommunicateAction):
    """The act of an agent communicating (service provider, social media, etc) their departure of a previously reserved service (e.g. flight check-in) or place (e.g. hotel).\\n\\nRelated actions:\\n\\n* [[CheckInAction]]: The antonym of CheckOutAction.\\n* [[DepartAction]]: Unlike DepartAction, CheckOutAction implies that the agent is informing/confirming the end of a previously reserved service.\\n* [[CancelAction]]: Unlike CancelAction, CheckOutAction implies that the agent is informing/confirming the end of a previously reserved service."""
    type: str = field(default_factory=lambda: "CheckOutAction", name="@type")