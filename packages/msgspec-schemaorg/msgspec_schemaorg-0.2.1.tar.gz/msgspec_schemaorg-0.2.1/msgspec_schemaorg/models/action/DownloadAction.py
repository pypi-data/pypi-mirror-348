from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import Optional, Union, Dict, List, Any


class DownloadAction(TransferAction):
    """The act of downloading an object."""
    type: str = field(default_factory=lambda: "DownloadAction", name="@type")