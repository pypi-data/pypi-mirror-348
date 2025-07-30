from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.OrganizeAction import OrganizeAction
from typing import Optional, Union, Dict, List, Any


class ApplyAction(OrganizeAction):
    """The act of registering to an organization/service without the guarantee to receive it.\\n\\nRelated actions:\\n\\n* [[RegisterAction]]: Unlike RegisterAction, ApplyAction has no guarantees that the application will be accepted."""
    type: str = field(default_factory=lambda: "ApplyAction", name="@type")