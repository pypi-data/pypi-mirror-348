from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class Project(Organization):
    """An enterprise (potentially individual but typically collaborative), planned to achieve a particular aim.
Use properties from [[Organization]], [[subOrganization]]/[[parentOrganization]] to indicate project sub-structures. 
   """
    type: str = field(default_factory=lambda: "Project", name="@type")