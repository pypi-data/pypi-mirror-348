from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class CreateAction(Action):
    """The act of deliberately creating/producing/generating/building a result out of the agent."""
    type: str = field(default_factory=lambda: "CreateAction", name="@type")