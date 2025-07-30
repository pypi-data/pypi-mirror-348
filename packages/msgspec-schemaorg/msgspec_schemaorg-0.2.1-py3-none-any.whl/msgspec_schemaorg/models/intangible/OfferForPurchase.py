from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Offer import Offer
from typing import Optional, Union, Dict, List, Any


class OfferForPurchase(Offer):
    """An [[OfferForPurchase]] in Schema.org represents an [[Offer]] to sell something, i.e. an [[Offer]] whose
  [[businessFunction]] is [sell](http://purl.org/goodrelations/v1#Sell.). See [Good Relations](https://en.wikipedia.org/wiki/GoodRelations) for
  background on the underlying concepts.
  """
    type: str = field(default_factory=lambda: "OfferForPurchase", name="@type")