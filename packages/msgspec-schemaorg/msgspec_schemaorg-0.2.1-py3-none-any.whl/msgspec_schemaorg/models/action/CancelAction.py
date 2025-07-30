from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.PlanAction import PlanAction
from typing import Optional, Union, Dict, List, Any


class CancelAction(PlanAction):
    """The act of asserting that a future event/action is no longer going to happen.\\n\\nRelated actions:\\n\\n* [[ConfirmAction]]: The antonym of CancelAction."""
    type: str = field(default_factory=lambda: "CancelAction", name="@type")