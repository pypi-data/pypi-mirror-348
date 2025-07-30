from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.DataFeed import DataFeed
from typing import Optional, Union, Dict, List, Any


class CompleteDataFeed(DataFeed):
    """A [[CompleteDataFeed]] is a [[DataFeed]] whose standard representation includes content for every item currently in the feed.

This is the equivalent of Atom's element as defined in Feed Paging and Archiving [RFC 5005](https://tools.ietf.org/html/rfc5005), for example (and as defined for Atom), when using data from a feed that represents a collection of items that varies over time (e.g. "Top Twenty Records") there is no need to have newer entries mixed in alongside older, obsolete entries. By marking this feed as a CompleteDataFeed, old entries can be safely discarded when the feed is refreshed, since we can assume the feed has provided descriptions for all current items."""
    type: str = field(default_factory=lambda: "CompleteDataFeed", name="@type")