from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas

class MaleoIdentityOrganizationRoleServiceParametersTransfers:
    class GetMultipleFromOrganizationQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultiple(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        BaseServiceParametersTransfers.GetPaginatedMultiple
    ): pass