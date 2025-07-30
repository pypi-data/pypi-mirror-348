from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Class import Class
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.models.intangible.Property import Property
from typing import Optional, Union, Dict, List, Any


class Property(Intangible):
    """A property, used to indicate attributes and relationships of some Thing; equivalent to rdf:Property."""
    type: str = field(default_factory=lambda: "Property", name="@type")
    supersededBy: Union[List[Union['Enumeration', 'Class', 'Property']], Union['Enumeration', 'Class', 'Property'], None] = None
    domainIncludes: Union[List['Class'], 'Class', None] = None
    inverseOf: Union[List['Property'], 'Property', None] = None
    rangeIncludes: Union[List['Class'], 'Class', None] = None