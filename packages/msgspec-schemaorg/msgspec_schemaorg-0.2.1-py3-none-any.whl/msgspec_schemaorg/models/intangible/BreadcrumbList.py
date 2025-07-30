from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class BreadcrumbList(ItemList):
    """A BreadcrumbList is an ItemList consisting of a chain of linked Web pages, typically described using at least their URL and their name, and typically ending with the current page.\\n\\nThe [[position]] property is used to reconstruct the order of the items in a BreadcrumbList. The convention is that a breadcrumb list has an [[itemListOrder]] of [[ItemListOrderAscending]] (lower values listed first), and that the first items in this list correspond to the "top" or beginning of the breadcrumb trail, e.g. with a site or section homepage. The specific values of 'position' are not assigned meaning for a BreadcrumbList, but they should be integers, e.g. beginning with '1' for the first item in the list.
      """
    type: str = field(default_factory=lambda: "BreadcrumbList", name="@type")