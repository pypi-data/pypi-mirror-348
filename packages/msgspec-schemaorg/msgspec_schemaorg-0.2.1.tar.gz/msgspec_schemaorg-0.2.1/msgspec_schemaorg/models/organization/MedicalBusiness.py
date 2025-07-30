from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import Optional, Union, Dict, List, Any


class MedicalBusiness(LocalBusiness):
    """A particular physical or virtual business of an organization for medical purposes. Examples of MedicalBusiness include different businesses run by health professionals."""
    type: str = field(default_factory=lambda: "MedicalBusiness", name="@type")