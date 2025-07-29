from pydantic import BaseModel, Field
from typing import Optional, List
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.types import BaseTypes
from maleo_identity.enums.organization_role import MaleoIdentityOrganizationRoleEnums

class MaleoIdentityOrganizationRoleGeneralSchemas:
    class Expand(BaseModel):
        expand:Optional[List[MaleoIdentityOrganizationRoleEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class OrganizationId(BaseModel):
        organization_id:int = Field(..., ge=1, description="Organization's ID")

    class OptionalListOfOrganizationId(BaseModel):
        organization_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Organization's IDs")

    class IsDefault(BaseModel):
        is_default:Optional[bool] = Field(None, description="Is default role")

    class Order(BaseGeneralSchemas.Order): pass

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=50, description="Organization Role's key")

    class OptionalListOfKey(BaseModel):
        keys:BaseTypes.OptionalListOfStrings = Field(None, description="Organization role's keys")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=50, description="Organization Role's name")