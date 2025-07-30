from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalIndication import MedicalIndication
from typing import Optional, Union, Dict, List, Any


class ApprovedIndication(MedicalIndication):
    """An indication for a medical therapy that has been formally specified or approved by a regulatory body that regulates use of the therapy; for example, the US FDA approves indications for most drugs in the US."""
    type: str = field(default_factory=lambda: "ApprovedIndication", name="@type")