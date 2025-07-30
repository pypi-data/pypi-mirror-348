from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.action.SolveMathAction import SolveMathAction
from typing import Optional, Union, Dict, List, Any


class MathSolver(CreativeWork):
    """A math solver which is capable of solving a subset of mathematical problems."""
    type: str = field(default_factory=lambda: "MathSolver", name="@type")
    mathExpression: Union[List[Union[str, 'SolveMathAction']], Union[str, 'SolveMathAction'], None] = None