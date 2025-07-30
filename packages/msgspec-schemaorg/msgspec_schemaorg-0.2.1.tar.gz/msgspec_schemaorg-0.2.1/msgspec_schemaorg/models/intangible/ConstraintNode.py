from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Property import Property
from typing import Optional, Union, Dict, List, Any


class ConstraintNode(Intangible):
    """The ConstraintNode type is provided to support usecases in which a node in a structured data graph is described with properties which appear to describe a single entity, but are being used in a situation where they serve a more abstract purpose. A [[ConstraintNode]] can be described using [[constraintProperty]] and [[numConstraints]]. These constraint properties can serve a
    variety of purposes, and their values may sometimes be understood to indicate sets of possible values rather than single, exact and specific values."""
    type: str = field(default_factory=lambda: "ConstraintNode", name="@type")
    numConstraints: Union[List[int], int, None] = None
    constraintProperty: Union[List[Union['URL', 'Property']], Union['URL', 'Property'], None] = None