from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from typing import Optional, Union, Dict, List, Any


class CssSelectorType(SchemaOrgBase):
    """Text representing a CSS selector."""
    type: str = field(default_factory=lambda: "CssSelectorType", name="@type")