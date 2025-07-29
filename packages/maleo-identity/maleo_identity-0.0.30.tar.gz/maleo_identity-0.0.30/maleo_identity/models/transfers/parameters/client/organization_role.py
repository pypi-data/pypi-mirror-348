from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas

class MaleoIdentityOrganizationRoleClientParametersTransfers:
    class GetMultipleFromOrganization(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OrganizationId
    ): pass
    
    class GetMultiple(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId
    ): pass