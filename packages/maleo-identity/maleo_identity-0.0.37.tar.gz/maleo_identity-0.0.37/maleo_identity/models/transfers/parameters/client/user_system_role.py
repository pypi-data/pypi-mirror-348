from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general.user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas

class MaleoIdentityUserSystemRoleClientParametersTransfers:
    class GetMultipleFromUser(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.UserId
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultipleFromUserQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId
    ): pass