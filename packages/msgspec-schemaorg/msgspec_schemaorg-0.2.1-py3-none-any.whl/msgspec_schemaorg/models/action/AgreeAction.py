from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ReactAction import ReactAction
from typing import Optional, Union, Dict, List, Any


class AgreeAction(ReactAction):
    """The act of expressing a consistency of opinion with the object. An agent agrees to/about an object (a proposition, topic or theme) with participants."""
    type: str = field(default_factory=lambda: "AgreeAction", name="@type")