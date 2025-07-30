from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.BankAccount import BankAccount
from typing import Optional, Union, Dict, List, Any


class DepositAccount(BankAccount):
    """A type of Bank Account with a main purpose of depositing funds to gain interest or other benefits."""
    type: str = field(default_factory=lambda: "DepositAccount", name="@type")