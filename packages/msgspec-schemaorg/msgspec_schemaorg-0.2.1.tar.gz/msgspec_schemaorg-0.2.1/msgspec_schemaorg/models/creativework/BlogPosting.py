from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.SocialMediaPosting import SocialMediaPosting
from typing import Optional, Union, Dict, List, Any


class BlogPosting(SocialMediaPosting):
    """A blog post."""
    type: str = field(default_factory=lambda: "BlogPosting", name="@type")