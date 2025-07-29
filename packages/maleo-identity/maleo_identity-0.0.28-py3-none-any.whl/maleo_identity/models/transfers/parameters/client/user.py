from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user import MaleoIdentityUserGeneralSchemas

class MaleoIdentityUserClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityUserGeneralSchemas.Expand,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoMetadataUserTypeExpandedSchemas.OptionalListOfSimpleUserType,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserGeneralSchemas.Expand,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoMetadataUserTypeExpandedSchemas.OptionalListOfSimpleUserType,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass