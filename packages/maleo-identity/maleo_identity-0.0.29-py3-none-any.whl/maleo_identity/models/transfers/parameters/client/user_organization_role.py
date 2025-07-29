from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas

class MaleoIdentityUserOrganizationRoleClientParametersTransfers:
    class GetMultipleFromUserOrOrganization(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.UserId
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultipleFromUserOrOrganizationQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId
    ): pass