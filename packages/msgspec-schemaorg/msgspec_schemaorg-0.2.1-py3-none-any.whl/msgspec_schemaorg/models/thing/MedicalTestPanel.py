from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import Optional, Union, Dict, List, Any


class MedicalTestPanel(MedicalTest):
    """Any collection of tests commonly ordered together."""
    type: str = field(default_factory=lambda: "MedicalTestPanel", name="@type")
    subTest: Union[List['MedicalTest'], 'MedicalTest', None] = None