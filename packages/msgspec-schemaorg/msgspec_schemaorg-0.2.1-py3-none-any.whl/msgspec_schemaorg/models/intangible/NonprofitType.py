from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class NonprofitType(Enumeration):
    """NonprofitType enumerates several kinds of official non-profit types of which a non-profit organization can be."""
    type: str = field(default_factory=lambda: "NonprofitType", name="@type")