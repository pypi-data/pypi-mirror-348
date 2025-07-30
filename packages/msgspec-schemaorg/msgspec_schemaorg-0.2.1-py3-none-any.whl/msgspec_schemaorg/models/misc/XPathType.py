from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from typing import Optional, Union, Dict, List, Any


class XPathType(SchemaOrgBase):
    """Text representing an XPath (typically but not necessarily version 1.0)."""
    type: str = field(default_factory=lambda: "XPathType", name="@type")