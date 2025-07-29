from pydantic import BaseModel, Field
from typing import Optional, List
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.enums.organization import MaleoIdentityOrganizationEnums

class MaleoIdentityOrganizationGeneralSchemas:
    class IdentifierType(BaseModel):
        identifier:MaleoIdentityOrganizationEnums.IdentifierType = Field(..., description="Organization's identifier")

    class Expand(BaseModel):
        expand:Optional[List[MaleoIdentityOrganizationEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class OptionalParentOrganizationId(BaseModel):
        parent_organization_id:BaseTypes.OptionalInteger = Field(None, ge=1, description="Parent organization's Id")

    class OptionalListOfParentOrganizationId(BaseModel):
        parent_organization_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Parent organization's Ids")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=255, description="Organization's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=255, description="Organization's name")