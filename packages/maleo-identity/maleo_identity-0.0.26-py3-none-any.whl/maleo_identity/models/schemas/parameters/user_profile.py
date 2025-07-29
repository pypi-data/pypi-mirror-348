from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user_profile import MaleoIdentityUserProfileGeneralSchemas

class MaleoIdentityUserProfileParametersSchemas:
    class Base(
        MaleoMetadataGenderExpandedSchemas.OptionalSimpleGender,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalSimpleBloodType,
        MaleoIdentityUserProfileGeneralSchemas.BirthDate,
        MaleoIdentityUserProfileGeneralSchemas.BirthPlace,
        MaleoIdentityUserProfileGeneralSchemas.EndingTitle,
        MaleoIdentityUserProfileGeneralSchemas.LastName,
        MaleoIdentityUserProfileGeneralSchemas.MiddleName,
        MaleoIdentityUserProfileGeneralSchemas.FirstName,
        MaleoIdentityUserProfileGeneralSchemas.LeadingTitle,
        MaleoIdentityUserProfileGeneralSchemas.IdCard
    ): pass

    class Extended(
        Base,
        MaleoIdentityUserProfileGeneralSchemas.UserId
    ): pass