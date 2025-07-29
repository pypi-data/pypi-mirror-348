from __future__ import annotations
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general.user import MaleoIdentityUserGeneralSchemas

class MaleoIdentityUserServiceParametersTransfers:
    class GetMultipleQuery(
        MaleoIdentityUserGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserGeneralSchemas.Phones,
        MaleoIdentityUserGeneralSchemas.Emails,
        MaleoIdentityUserGeneralSchemas.Usernames,
        MaleoMetadataUserTypeExpandedSchemas.OptionalListOfSimpleUserType,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultiple(
        MaleoIdentityUserGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodType,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGender,
        MaleoIdentityUserGeneralSchemas.Phones,
        MaleoIdentityUserGeneralSchemas.Emails,
        MaleoIdentityUserGeneralSchemas.Usernames,
        MaleoMetadataUserTypeExpandedSchemas.OptionalListOfSimpleUserType,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass