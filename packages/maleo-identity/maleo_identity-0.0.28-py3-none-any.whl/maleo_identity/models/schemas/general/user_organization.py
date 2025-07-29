from pydantic import BaseModel, Field
from typing import Optional, List
from maleo_foundation.types import BaseTypes
from maleo_identity.enums.user_organization import MaleoIdentityUserOrganizationEnums

class MaleoIdentityUserOrganizationGeneralSchemas:
    class Expand(BaseModel):
        expand:Optional[List[MaleoIdentityUserOrganizationEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class UserId(BaseModel):
        user_id:int = Field(..., ge=1, description="User's ID")

    class OptionalListOfUserId(BaseModel):
        user_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="User's IDs")

    class OrganizationId(BaseModel):
        organization_id:int = Field(..., ge=1, description="Organization's ID")

    class OptionalListOfOrganizationId(BaseModel):
        organization_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Organization's IDs")