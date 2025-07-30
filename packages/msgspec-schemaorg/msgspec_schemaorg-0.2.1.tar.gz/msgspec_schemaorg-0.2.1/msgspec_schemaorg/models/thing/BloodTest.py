from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import Optional, Union, Dict, List, Any


class BloodTest(MedicalTest):
    """A medical test performed on a sample of a patient's blood."""
    type: str = field(default_factory=lambda: "BloodTest", name="@type")