from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Project import Project
from typing import Optional, Union, Dict, List, Any


class ResearchProject(Project):
    """A Research project."""
    type: str = field(default_factory=lambda: "ResearchProject", name="@type")