from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas

class MaleoIdentityUserOrganizationRoleClientParametersTransfers:
    class GetMultipleFromUserOrOrganization(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.UserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleFromUserOrOrganizationQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass