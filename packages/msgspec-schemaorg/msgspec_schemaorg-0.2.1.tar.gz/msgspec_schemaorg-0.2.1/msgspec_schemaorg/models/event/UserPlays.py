from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.UserInteraction import UserInteraction
from typing import Optional, Union, Dict, List, Any


class UserPlays(UserInteraction):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]]."""
    type: str = field(default_factory=lambda: "UserPlays", name="@type")