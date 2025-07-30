from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import Optional, Union, Dict, List, Any


class TakeAction(TransferAction):
    """The act of gaining ownership of an object from an origin. Reciprocal of GiveAction.\\n\\nRelated actions:\\n\\n* [[GiveAction]]: The reciprocal of TakeAction.\\n* [[ReceiveAction]]: Unlike ReceiveAction, TakeAction implies that ownership has been transferred."""
    type: str = field(default_factory=lambda: "TakeAction", name="@type")