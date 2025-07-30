from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Dataset import Dataset
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DataFeedItem import DataFeedItem
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class DataFeed(Dataset):
    """A single feed providing structured information about one or more entities or topics."""
    type: str = field(default_factory=lambda: "DataFeed", name="@type")
    dataFeedElement: Union[List[Union[str, 'DataFeedItem', 'Thing']], Union[str, 'DataFeedItem', 'Thing'], None] = None