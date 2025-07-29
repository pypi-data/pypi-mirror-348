from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user_profile import MaleoIdentityUserProfileGeneralSchemas

class MaleoIdentityUserProfileServiceParametersTransfers:
    class GetMultipleQuery(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultiple(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultiple
    ): pass