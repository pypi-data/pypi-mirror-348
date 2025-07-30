from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Offer import Offer
from typing import Optional, Union, Dict, List, Any


class OfferForLease(Offer):
    """An [[OfferForLease]] in Schema.org represents an [[Offer]] to lease out something, i.e. an [[Offer]] whose
  [[businessFunction]] is [lease out](http://purl.org/goodrelations/v1#LeaseOut.). See [Good Relations](https://en.wikipedia.org/wiki/GoodRelations) for
  background on the underlying concepts.
  """
    type: str = field(default_factory=lambda: "OfferForLease", name="@type")