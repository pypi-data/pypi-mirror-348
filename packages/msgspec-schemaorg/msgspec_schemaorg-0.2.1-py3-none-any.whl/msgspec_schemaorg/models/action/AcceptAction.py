from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AllocateAction import AllocateAction
from typing import Optional, Union, Dict, List, Any


class AcceptAction(AllocateAction):
    """The act of committing to/adopting an object.\\n\\nRelated actions:\\n\\n* [[RejectAction]]: The antonym of AcceptAction."""
    type: str = field(default_factory=lambda: "AcceptAction", name="@type")