from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user_profile import MaleoIdentityUserProfileGeneralSchemas

class MaleoIdentityUserProfileResultsSchemas:
    class General(
        MaleoMetadataBloodTypeExpandedSchemas.OptionalExpandedBloodType,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalExpandedGender,
        MaleoMetadataGenderExpandedSchemas.OptionalSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.BirthDate,
        MaleoIdentityUserProfileGeneralSchemas.BirthPlace,
        MaleoIdentityUserProfileGeneralSchemas.EndingTitle,
        MaleoIdentityUserProfileGeneralSchemas.LastName,
        MaleoIdentityUserProfileGeneralSchemas.MiddleName,
        MaleoIdentityUserProfileGeneralSchemas.FirstName,
        MaleoIdentityUserProfileGeneralSchemas.LeadingTitle,
        MaleoIdentityUserProfileGeneralSchemas.IdCard,
        MaleoIdentityUserProfileGeneralSchemas.UserId
    ): pass

    class Query(
        MaleoMetadataBloodTypeExpandedSchemas.OptionalSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.BirthDate,
        MaleoIdentityUserProfileGeneralSchemas.BirthPlace,
        MaleoIdentityUserProfileGeneralSchemas.EndingTitle,
        MaleoIdentityUserProfileGeneralSchemas.LastName,
        MaleoIdentityUserProfileGeneralSchemas.MiddleName,
        MaleoIdentityUserProfileGeneralSchemas.FirstName,
        MaleoIdentityUserProfileGeneralSchemas.LeadingTitle,
        MaleoIdentityUserProfileGeneralSchemas.IdCard,
        MaleoIdentityUserProfileGeneralSchemas.UserId
    ): pass