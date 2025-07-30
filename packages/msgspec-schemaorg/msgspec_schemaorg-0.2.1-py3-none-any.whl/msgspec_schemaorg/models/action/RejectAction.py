from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AllocateAction import AllocateAction
from typing import Optional, Union, Dict, List, Any


class RejectAction(AllocateAction):
    """The act of rejecting to/adopting an object.\\n\\nRelated actions:\\n\\n* [[AcceptAction]]: The antonym of RejectAction."""
    type: str = field(default_factory=lambda: "RejectAction", name="@type")