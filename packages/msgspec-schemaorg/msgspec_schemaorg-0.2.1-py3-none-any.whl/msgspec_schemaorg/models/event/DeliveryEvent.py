from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from msgspec_schemaorg.utils import parse_iso8601
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DeliveryMethod import DeliveryMethod
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class DeliveryEvent(Event):
    """An event involving the delivery of an item."""
    type: str = field(default_factory=lambda: "DeliveryEvent", name="@type")
    availableFrom: Union[List[datetime], datetime, None] = None
    hasDeliveryMethod: Union[List['DeliveryMethod'], 'DeliveryMethod', None] = None
    availableThrough: Union[List[datetime], datetime, None] = None
    accessCode: Union[List[str], str, None] = None