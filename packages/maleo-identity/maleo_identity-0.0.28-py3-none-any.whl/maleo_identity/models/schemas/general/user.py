from pydantic import BaseModel, Field
from typing import Optional, List
from maleo_identity.enums.user import MaleoIdentityUserEnums

class MaleoIdentityUserGeneralSchemas:
    class IdentifierType(BaseModel):
        identifier:MaleoIdentityUserEnums.IdentifierType = Field(..., description="User's identifier")

    class Expand(BaseModel):
        expand:Optional[List[MaleoIdentityUserEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class Username(BaseModel):
        username:str = Field(..., max_length=50, description="User's username")

    class Email(BaseModel):
        email:str = Field(..., max_length=255, description="User's email")

    class Phone(BaseModel):
        phone:str = Field(..., max_length=15, description="User's username")

    class Password(BaseModel):
        password:str = Field(..., max_length=255, description="User's password")