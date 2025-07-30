from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
from typing import Optional, Union, Dict, List, Any


class Barcode(ImageObject):
    """An image of a visual machine-readable code such as a barcode or QR code."""
    type: str = field(default_factory=lambda: "Barcode", name="@type")