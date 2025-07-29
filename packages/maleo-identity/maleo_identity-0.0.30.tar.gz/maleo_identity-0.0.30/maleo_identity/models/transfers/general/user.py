from pydantic import BaseModel, Field
from typing import Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.results.user import MaleoIdentityUserResultsSchemas
from maleo_identity.models.transfers.general.user_profile import OptionalExpandedUserProfile

class UserTransfers(
    OptionalExpandedUserProfile,
    MaleoIdentityUserResultsSchemas.General,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass

class OptionalExpandedUser(BaseModel):
    user_details:Optional[UserTransfers] = Field(None, description="User's details")

class PasswordTransfers(MaleoIdentityUserResultsSchemas.PasswordGeneral): pass