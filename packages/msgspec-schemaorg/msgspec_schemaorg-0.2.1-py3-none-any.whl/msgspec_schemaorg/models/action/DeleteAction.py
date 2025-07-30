from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.UpdateAction import UpdateAction
from typing import Optional, Union, Dict, List, Any


class DeleteAction(UpdateAction):
    """The act of editing a recipient by removing one of its objects."""
    type: str = field(default_factory=lambda: "DeleteAction", name="@type")