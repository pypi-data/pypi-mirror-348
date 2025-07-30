from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.TransferAction import TransferAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class BorrowAction(TransferAction):
    """The act of obtaining an object under an agreement to return it at a later date. Reciprocal of LendAction.\\n\\nRelated actions:\\n\\n* [[LendAction]]: Reciprocal of BorrowAction."""
    type: str = field(default_factory=lambda: "BorrowAction", name="@type")
    lender: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None