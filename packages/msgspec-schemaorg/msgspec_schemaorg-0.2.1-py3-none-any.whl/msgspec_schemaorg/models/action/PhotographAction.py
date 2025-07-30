from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CreateAction import CreateAction
from typing import Optional, Union, Dict, List, Any


class PhotographAction(CreateAction):
    """The act of capturing still images of objects using a camera."""
    type: str = field(default_factory=lambda: "PhotographAction", name="@type")