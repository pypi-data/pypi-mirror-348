from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas

class MaleoIdentityOrganizationRoleClientParametersTransfers:
    class GetMultipleFromOrganization(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OrganizationId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass
    
    class GetMultiple(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass