from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.TechArticle import TechArticle
from typing import Optional, Union, Dict, List, Any


class APIReference(TechArticle):
    """Reference documentation for application programming interfaces (APIs)."""
    type: str = field(default_factory=lambda: "APIReference", name="@type")
    executableLibraryName: Union[List[str], str, None] = None
    targetPlatform: Union[List[str], str, None] = None
    programmingModel: Union[List[str], str, None] = None
    assembly: Union[List[str], str, None] = None
    assemblyVersion: Union[List[str], str, None] = None