from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class DryCleaningOrLaundry(LocalBusiness):
    """A dry-cleaning business."""
    type: str = field(default_factory=lambda: "DryCleaningOrLaundry", name="@type")