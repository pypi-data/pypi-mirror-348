from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class SizeGroupEnumeration(Enumeration):
    """Enumerates common size groups for various product categories."""
    type: str = field(default_factory=lambda: "SizeGroupEnumeration", name="@type")