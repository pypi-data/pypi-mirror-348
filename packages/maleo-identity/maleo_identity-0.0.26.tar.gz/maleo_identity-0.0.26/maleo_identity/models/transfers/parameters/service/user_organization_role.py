from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas

class MaleoIdentityUserOrganizationRoleServiceParametersTransfers:
    class GetMultipleFromUserOrOrganizationQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultiple(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultiple
    ): pass