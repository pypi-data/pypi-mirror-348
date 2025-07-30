from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MediaEnumeration(Enumeration):
    """MediaEnumeration enumerations are lists of codes, labels etc. useful for describing media objects. They may be reflections of externally developed lists, or created at schema.org, or a combination."""
    type: str = field(default_factory=lambda: "MediaEnumeration", name="@type")