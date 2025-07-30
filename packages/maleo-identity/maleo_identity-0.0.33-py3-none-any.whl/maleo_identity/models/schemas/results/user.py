from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_identity.models.schemas.general.user import MaleoIdentityUserGeneralSchemas

class MaleoIdentityUserResultsSchemas:
    class General(
        MaleoIdentityUserGeneralSchemas.Phone,
        MaleoIdentityUserGeneralSchemas.Email,
        MaleoIdentityUserGeneralSchemas.Username,
        MaleoMetadataUserTypeExpandedSchemas.OptionalExpandedUserType,
        MaleoMetadataUserTypeExpandedSchemas.SimpleUserType
    ): pass

    class PasswordGeneral(MaleoIdentityUserGeneralSchemas.Password): pass

    class Query(
        MaleoIdentityUserGeneralSchemas.Phone,
        MaleoIdentityUserGeneralSchemas.Email,
        MaleoIdentityUserGeneralSchemas.Username,
        MaleoMetadataUserTypeExpandedSchemas.SimpleUserType
    ): pass

    class PasswordQuery(MaleoIdentityUserGeneralSchemas.Password): pass