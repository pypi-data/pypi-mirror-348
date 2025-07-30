from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from typing import Optional, Union, Dict, List, Any


class URL(SchemaOrgBase):
    """Data type: URL."""
    type: str = field(default_factory=lambda: "URL", name="@type")