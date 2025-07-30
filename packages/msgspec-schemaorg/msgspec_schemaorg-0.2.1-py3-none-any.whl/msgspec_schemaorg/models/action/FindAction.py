from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class FindAction(Action):
    """The act of finding an object.\\n\\nRelated actions:\\n\\n* [[SearchAction]]: FindAction is generally lead by a SearchAction, but not necessarily."""
    type: str = field(default_factory=lambda: "FindAction", name="@type")