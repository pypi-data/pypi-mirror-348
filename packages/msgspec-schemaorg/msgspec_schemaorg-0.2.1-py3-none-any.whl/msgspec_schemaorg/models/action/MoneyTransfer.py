from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.organization.BankOrCreditUnion import BankOrCreditUnion
from typing import Optional, Union, Dict, List, Any


class MoneyTransfer(TransferAction):
    """The act of transferring money from one place to another place. This may occur electronically or physically."""
    type: str = field(default_factory=lambda: "MoneyTransfer", name="@type")
    beneficiaryBank: Union[List[Union[str, 'BankOrCreditUnion']], Union[str, 'BankOrCreditUnion'], None] = None
    amount: Union[List[Union[int | float, 'MonetaryAmount']], Union[int | float, 'MonetaryAmount'], None] = None