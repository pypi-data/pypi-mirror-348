from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.intangible.Audience import Audience
from typing import Optional, Union, Dict, List, Any


class PlayAction(Action):
    """The act of playing/exercising/training/performing for enjoyment, leisure, recreation, competition or exercise.\\n\\nRelated actions:\\n\\n* [[ListenAction]]: Unlike ListenAction (which is under ConsumeAction), PlayAction refers to performing for an audience or at an event, rather than consuming music.\\n* [[WatchAction]]: Unlike WatchAction (which is under ConsumeAction), PlayAction refers to showing/displaying for an audience or at an event, rather than consuming visual content."""
    type: str = field(default_factory=lambda: "PlayAction", name="@type")
    event: Union[List['Event'], 'Event', None] = None
    audience: Union[List['Audience'], 'Audience', None] = None