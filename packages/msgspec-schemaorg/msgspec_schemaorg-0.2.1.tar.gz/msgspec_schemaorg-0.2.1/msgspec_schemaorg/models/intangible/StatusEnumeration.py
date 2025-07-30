from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class StatusEnumeration(Enumeration):
    """Lists or enumerations dealing with status types."""
    type: str = field(default_factory=lambda: "StatusEnumeration", name="@type")