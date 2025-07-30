from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWorkSeries import CreativeWorkSeries
from typing import Optional, Union, Dict, List, Any


class Periodical(CreativeWorkSeries):
    """A publication in any medium issued in successive parts bearing numerical or chronological designations and intended to continue indefinitely, such as a magazine, scholarly journal, or newspaper.\\n\\nSee also [blog post](http://blog.schema.org/2014/09/schemaorg-support-for-bibliographic_2.html)."""
    type: str = field(default_factory=lambda: "Periodical", name="@type")