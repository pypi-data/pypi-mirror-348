from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Project import Project
from typing import Optional, Union, Dict, List, Any


class FundingAgency(Project):
    """A FundingAgency is an organization that implements one or more [[FundingScheme]]s and manages
    the granting process (via [[Grant]]s, typically [[MonetaryGrant]]s).
    A funding agency is not always required for grant funding, e.g. philanthropic giving, corporate sponsorship etc.
    
Examples of funding agencies include ERC, REA, NIH, Bill and Melinda Gates Foundation, ...
    """
    type: str = field(default_factory=lambda: "FundingAgency", name="@type")