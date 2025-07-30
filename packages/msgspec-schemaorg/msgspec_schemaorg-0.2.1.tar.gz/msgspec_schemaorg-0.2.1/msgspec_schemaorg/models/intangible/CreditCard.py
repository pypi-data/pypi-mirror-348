from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PaymentCard import PaymentCard
from typing import Optional, Union, Dict, List, Any


class CreditCard(PaymentCard):
    """A card payment method of a particular brand or name.  Used to mark up a particular payment method and/or the financial product/service that supplies the card account.\\n\\nCommonly used values:\\n\\n* http://purl.org/goodrelations/v1#AmericanExpress\\n* http://purl.org/goodrelations/v1#DinersClub\\n* http://purl.org/goodrelations/v1#Discover\\n* http://purl.org/goodrelations/v1#JCB\\n* http://purl.org/goodrelations/v1#MasterCard\\n* http://purl.org/goodrelations/v1#VISA
       """
    type: str = field(default_factory=lambda: "CreditCard", name="@type")