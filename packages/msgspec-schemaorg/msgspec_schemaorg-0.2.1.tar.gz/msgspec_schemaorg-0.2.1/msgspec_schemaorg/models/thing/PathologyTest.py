from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import Optional, Union, Dict, List, Any


class PathologyTest(MedicalTest):
    """A medical test performed by a laboratory that typically involves examination of a tissue sample by a pathologist."""
    type: str = field(default_factory=lambda: "PathologyTest", name="@type")
    tissueSample: Union[List[str], str, None] = None