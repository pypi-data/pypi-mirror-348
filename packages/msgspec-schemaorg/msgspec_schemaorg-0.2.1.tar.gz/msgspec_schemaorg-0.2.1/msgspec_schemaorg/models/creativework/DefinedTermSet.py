from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
from typing import Optional, Union, Dict, List, Any


class DefinedTermSet(CreativeWork):
    """A set of defined terms, for example a set of categories or a classification scheme, a glossary, dictionary or enumeration."""
    type: str = field(default_factory=lambda: "DefinedTermSet", name="@type")
    hasDefinedTerm: Union[List['DefinedTerm'], 'DefinedTerm', None] = None