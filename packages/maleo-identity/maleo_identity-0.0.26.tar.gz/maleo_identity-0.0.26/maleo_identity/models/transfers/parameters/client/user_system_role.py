from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general.user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas

class MaleoIdentityUserSystemRoleClientParametersTransfers:
    class GetMultipleFromUser(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.UserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleFromUserQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass