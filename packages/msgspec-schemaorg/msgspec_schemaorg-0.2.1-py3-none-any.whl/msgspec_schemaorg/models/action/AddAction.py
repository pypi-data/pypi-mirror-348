from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.UpdateAction import UpdateAction
from typing import Optional, Union, Dict, List, Any


class AddAction(UpdateAction):
    """The act of editing by adding an object to a collection."""
    type: str = field(default_factory=lambda: "AddAction", name="@type")