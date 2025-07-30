from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class OfferCatalog(ItemList):
    """An OfferCatalog is an ItemList that contains related Offers and/or further OfferCatalogs that are offeredBy the same provider."""
    type: str = field(default_factory=lambda: "OfferCatalog", name="@type")