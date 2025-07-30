from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InformAction import InformAction
from typing import Optional, Union, Dict, List, Any


class ConfirmAction(InformAction):
    """The act of notifying someone that a future event/action is going to happen as expected.\\n\\nRelated actions:\\n\\n* [[CancelAction]]: The antonym of ConfirmAction."""
    type: str = field(default_factory=lambda: "ConfirmAction", name="@type")