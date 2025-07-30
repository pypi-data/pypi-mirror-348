from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AllocateAction import AllocateAction
from typing import Optional, Union, Dict, List, Any


class AssignAction(AllocateAction):
    """The act of allocating an action/event/task to some destination (someone or something)."""
    type: str = field(default_factory=lambda: "AssignAction", name="@type")