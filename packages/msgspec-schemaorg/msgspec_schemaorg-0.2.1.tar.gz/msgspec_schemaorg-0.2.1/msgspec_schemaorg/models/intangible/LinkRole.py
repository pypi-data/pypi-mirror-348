from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Role import Role
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class LinkRole(Role):
    """A Role that represents a Web link, e.g. as expressed via the 'url' property. Its linkRelationship property can indicate URL-based and plain textual link types, e.g. those in IANA link registry or others such as 'amphtml'. This structure provides a placeholder where details from HTML's link element can be represented outside of HTML, e.g. in JSON-LD feeds."""
    type: str = field(default_factory=lambda: "LinkRole", name="@type")
    linkRelationship: Union[List[str], str, None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None