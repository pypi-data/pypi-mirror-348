from pydantic import BaseModel, Field
from typing import Optional, List
from maleo_foundation.types import BaseTypes
from maleo_identity.enums.user_system_role import MaleoIdentityUserSystemRoleEnums

class MaleoIdentityUserSystemRoleGeneralSchemas:
    class Expand(BaseModel):
        expand:Optional[List[MaleoIdentityUserSystemRoleEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class UserId(BaseModel):
        user_id:int = Field(..., ge=1, description="User's ID")

    class OptionalListOfUserId(BaseModel):
        user_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="User's IDs")