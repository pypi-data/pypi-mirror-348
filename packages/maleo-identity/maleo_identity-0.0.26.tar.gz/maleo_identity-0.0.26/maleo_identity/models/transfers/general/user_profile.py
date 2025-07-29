from pydantic import BaseModel, Field
from typing import Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.results.user_profile import MaleoIdentityUserProfileResultsSchemas

class UserProfileTransfers(
    MaleoIdentityUserProfileResultsSchemas.General,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass

class OptionalExpandedUserProfile(BaseModel):
    profile:Optional[UserProfileTransfers] = Field(None, description="User's profile")