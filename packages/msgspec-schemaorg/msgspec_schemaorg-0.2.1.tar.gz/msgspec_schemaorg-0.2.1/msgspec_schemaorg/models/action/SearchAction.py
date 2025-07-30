from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class SearchAction(Action):
    """The act of searching for an object.\\n\\nRelated actions:\\n\\n* [[FindAction]]: SearchAction generally leads to a FindAction, but not necessarily."""
    type: str = field(default_factory=lambda: "SearchAction", name="@type")
    query: Union[List[str], str, None] = None