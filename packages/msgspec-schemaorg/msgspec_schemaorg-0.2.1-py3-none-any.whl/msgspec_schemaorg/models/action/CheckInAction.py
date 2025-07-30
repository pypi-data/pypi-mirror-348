from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import Optional, Union, Dict, List, Any


class CheckInAction(CommunicateAction):
    """The act of an agent communicating (service provider, social media, etc) their arrival by registering/confirming for a previously reserved service (e.g. flight check-in) or at a place (e.g. hotel), possibly resulting in a result (boarding pass, etc).\\n\\nRelated actions:\\n\\n* [[CheckOutAction]]: The antonym of CheckInAction.\\n* [[ArriveAction]]: Unlike ArriveAction, CheckInAction implies that the agent is informing/confirming the start of a previously reserved service.\\n* [[ConfirmAction]]: Unlike ConfirmAction, CheckInAction implies that the agent is informing/confirming the *start* of a previously reserved service rather than its validity/existence."""
    type: str = field(default_factory=lambda: "CheckInAction", name="@type")