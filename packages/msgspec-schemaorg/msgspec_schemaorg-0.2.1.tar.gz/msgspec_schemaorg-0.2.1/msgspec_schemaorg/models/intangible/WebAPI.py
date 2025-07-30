from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class WebAPI(Service):
    """An application programming interface accessible over Web/Internet technologies."""
    type: str = field(default_factory=lambda: "WebAPI", name="@type")
    documentation: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None