from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Store import Store
from typing import Optional, Union, Dict, List, Any


class DepartmentStore(Store):
    """A department store."""
    type: str = field(default_factory=lambda: "DepartmentStore", name="@type")