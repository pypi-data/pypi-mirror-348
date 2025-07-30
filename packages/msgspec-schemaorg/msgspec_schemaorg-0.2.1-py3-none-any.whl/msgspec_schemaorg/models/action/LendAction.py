from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class LendAction(TransferAction):
    """The act of providing an object under an agreement that it will be returned at a later date. Reciprocal of BorrowAction.\\n\\nRelated actions:\\n\\n* [[BorrowAction]]: Reciprocal of LendAction."""
    type: str = field(default_factory=lambda: "LendAction", name="@type")
    borrower: Union[List['Person'], 'Person', None] = None