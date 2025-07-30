from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.OrganizeAction import OrganizeAction
from typing import Optional, Union, Dict, List, Any


class BookmarkAction(OrganizeAction):
    """An agent bookmarks/flags/labels/tags/marks an object."""
    type: str = field(default_factory=lambda: "BookmarkAction", name="@type")