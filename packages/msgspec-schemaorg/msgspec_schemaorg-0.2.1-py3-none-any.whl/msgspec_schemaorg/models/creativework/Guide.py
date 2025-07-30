from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Guide(CreativeWork):
    """[[Guide]] is a page or article that recommends specific products or services, or aspects of a thing for a user to consider. A [[Guide]] may represent a Buying Guide and detail aspects of products or services for a user to consider. A [[Guide]] may represent a Product Guide and recommend specific products or services. A [[Guide]] may represent a Ranked List and recommend specific products or services with ranking."""
    type: str = field(default_factory=lambda: "Guide", name="@type")
    reviewAspect: Union[List[str], str, None] = None