from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DigitalDocumentPermission import DigitalDocumentPermission
from typing import Optional, Union, Dict, List, Any


class DigitalDocument(CreativeWork):
    """An electronic file or document."""
    type: str = field(default_factory=lambda: "DigitalDocument", name="@type")
    hasDigitalDocumentPermission: Union[List['DigitalDocumentPermission'], 'DigitalDocumentPermission', None] = None