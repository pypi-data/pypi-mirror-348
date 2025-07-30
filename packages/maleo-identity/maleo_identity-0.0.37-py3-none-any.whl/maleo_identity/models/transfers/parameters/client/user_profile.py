from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user_profile import MaleoIdentityUserProfileGeneralSchemas

class MaleoIdentityUserProfileClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserProfileGeneralSchemas.OptionalListOfUserId
    ): pass