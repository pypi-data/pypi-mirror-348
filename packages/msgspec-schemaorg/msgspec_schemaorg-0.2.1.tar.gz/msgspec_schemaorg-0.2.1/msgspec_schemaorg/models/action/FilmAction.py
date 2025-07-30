from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CreateAction import CreateAction
from typing import Optional, Union, Dict, List, Any


class FilmAction(CreateAction):
    """The act of capturing sound and moving images on film, video, or digitally."""
    type: str = field(default_factory=lambda: "FilmAction", name="@type")