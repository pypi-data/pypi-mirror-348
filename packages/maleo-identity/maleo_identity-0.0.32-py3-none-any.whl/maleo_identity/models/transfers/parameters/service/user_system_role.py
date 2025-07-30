from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general.user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas

class MaleoIdentityUserSystemRoleServiceParametersTransfers:
    class GetMultipleFromUserQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultiple(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId
    ): pass