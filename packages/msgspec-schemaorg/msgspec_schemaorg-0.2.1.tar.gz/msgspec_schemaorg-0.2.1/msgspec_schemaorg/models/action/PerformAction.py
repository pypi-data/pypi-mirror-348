from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.PlayAction import PlayAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.EntertainmentBusiness import EntertainmentBusiness
from typing import Optional, Union, Dict, List, Any


class PerformAction(PlayAction):
    """The act of participating in performance arts."""
    type: str = field(default_factory=lambda: "PerformAction", name="@type")
    entertainmentBusiness: Union[List['EntertainmentBusiness'], 'EntertainmentBusiness', None] = None