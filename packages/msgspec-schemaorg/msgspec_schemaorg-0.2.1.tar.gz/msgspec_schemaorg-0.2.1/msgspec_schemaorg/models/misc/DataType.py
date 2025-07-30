from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from typing import Optional, Union, Dict, List, Any


class DataType(SchemaOrgBase):
    """The basic data types such as Integers, Strings, etc."""
    type: str = field(default_factory=lambda: "DataType", name="@type")