from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class Code(CreativeWork):
    """Computer programming source code. Example: Full (compile ready) solutions, code snippet samples, scripts, templates."""
    type: str = field(default_factory=lambda: "Code", name="@type")