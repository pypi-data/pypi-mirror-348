from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.PaymentMethod import PaymentMethod
from typing import Optional, Union, Dict, List, Any


class PaymentService(PaymentMethod):
    """A Service to transfer funds from a person or organization to a beneficiary person or organization."""
    type: str = field(default_factory=lambda: "PaymentService", name="@type")