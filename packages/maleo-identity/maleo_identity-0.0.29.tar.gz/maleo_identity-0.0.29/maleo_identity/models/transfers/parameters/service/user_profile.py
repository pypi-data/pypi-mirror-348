from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user_profile import MaleoIdentityUserProfileGeneralSchemas

class MaleoIdentityUserProfileServiceParametersTransfers:
    class GetMultipleQuery(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultiple(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.OptionalListOfUserId
    ): pass