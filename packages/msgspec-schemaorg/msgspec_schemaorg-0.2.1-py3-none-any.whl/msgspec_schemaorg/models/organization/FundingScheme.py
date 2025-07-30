from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class FundingScheme(Organization):
    """A FundingScheme combines organizational, project and policy aspects of grant-based funding
    that sets guidelines, principles and mechanisms to support other kinds of projects and activities.
    Funding is typically organized via [[Grant]] funding. Examples of funding schemes: Swiss Priority Programmes (SPPs); EU Framework 7 (FP7); Horizon 2020; the NIH-R01 Grant Program; Wellcome institutional strategic support fund. For large scale public sector funding, the management and administration of grant awards is often handled by other, dedicated, organizations - [[FundingAgency]]s such as ERC, REA, ..."""
    type: str = field(default_factory=lambda: "FundingScheme", name="@type")