from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Class import Class
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.models.intangible.Property import Property
from typing import Optional, Union, Dict, List, Any


class Class(Intangible):
    """A class, also often called a 'Type'; equivalent to rdfs:Class."""
    type: str = field(default_factory=lambda: "Class", name="@type")
    supersededBy: Union[List[Union['Enumeration', 'Class', 'Property']], Union['Enumeration', 'Class', 'Property'], None] = None