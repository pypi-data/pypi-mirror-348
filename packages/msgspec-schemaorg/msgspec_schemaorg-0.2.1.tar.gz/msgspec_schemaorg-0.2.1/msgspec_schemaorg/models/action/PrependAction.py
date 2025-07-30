from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InsertAction import InsertAction
from typing import Optional, Union, Dict, List, Any


class PrependAction(InsertAction):
    """The act of inserting at the beginning if an ordered collection."""
    type: str = field(default_factory=lambda: "PrependAction", name="@type")