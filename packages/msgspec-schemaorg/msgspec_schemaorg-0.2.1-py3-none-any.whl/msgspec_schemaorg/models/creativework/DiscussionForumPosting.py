from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.SocialMediaPosting import SocialMediaPosting
from typing import Optional, Union, Dict, List, Any


class DiscussionForumPosting(SocialMediaPosting):
    """A posting to a discussion forum."""
    type: str = field(default_factory=lambda: "DiscussionForumPosting", name="@type")