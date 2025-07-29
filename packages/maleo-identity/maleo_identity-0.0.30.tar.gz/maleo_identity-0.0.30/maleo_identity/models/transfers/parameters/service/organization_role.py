from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas

class MaleoIdentityOrganizationRoleServiceParametersTransfers:
    class GetMultipleFromOrganizationQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId
    ): pass

    class GetMultiple(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId
    ): pass