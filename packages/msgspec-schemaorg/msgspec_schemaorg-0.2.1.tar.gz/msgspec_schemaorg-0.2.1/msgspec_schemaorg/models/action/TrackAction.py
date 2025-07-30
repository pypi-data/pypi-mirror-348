from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.FindAction import FindAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
from typing import Optional, Union, Dict, List, Any


class TrackAction(FindAction):
    """An agent tracks an object for updates.\\n\\nRelated actions:\\n\\n* [[FollowAction]]: Unlike FollowAction, TrackAction refers to the interest on the location of innanimates objects.\\n* [[SubscribeAction]]: Unlike SubscribeAction, TrackAction refers to  the interest on the location of innanimate objects."""
    type: str = field(default_factory=lambda: "TrackAction", name="@type")
    deliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None