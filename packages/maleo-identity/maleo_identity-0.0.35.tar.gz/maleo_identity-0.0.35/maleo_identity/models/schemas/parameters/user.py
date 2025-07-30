from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_identity.models.schemas.general.user import MaleoIdentityUserGeneralSchemas

class MaleoIdentityUserParametersSchemas:
    class Base(
        MaleoIdentityUserGeneralSchemas.Phone,
        MaleoIdentityUserGeneralSchemas.Email,
        MaleoIdentityUserGeneralSchemas.Username,
        MaleoMetadataUserTypeExpandedSchemas.SimpleUserType
    ): pass

    class Extended(
        MaleoIdentityUserGeneralSchemas.Password,
        Base
    ): pass