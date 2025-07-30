from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
from typing import Optional, Union, Dict, List, Any


class BedType(QualitativeValue):
    """A type of bed. This is used for indicating the bed or beds available in an accommodation."""
    type: str = field(default_factory=lambda: "BedType", name="@type")