from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LodgingBusiness import LodgingBusiness
from typing import Optional, Union, Dict, List, Any


class Hostel(LodgingBusiness):
    """A hostel - cheap accommodation, often in shared dormitories.
<br /><br />
See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.
"""
    type: str = field(default_factory=lambda: "Hostel", name="@type")