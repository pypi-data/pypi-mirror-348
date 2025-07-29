from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general.user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas

class MaleoIdentityUserSystemRoleServiceParametersTransfers:
    class GetMultipleFromUserQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultiple(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultiple
    ): pass