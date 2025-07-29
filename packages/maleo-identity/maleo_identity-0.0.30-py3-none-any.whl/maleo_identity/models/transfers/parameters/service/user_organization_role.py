from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas

class MaleoIdentityUserOrganizationRoleServiceParametersTransfers:
    class GetMultipleFromUserOrOrganizationQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultiple(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfKey,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OptionalListOfUserId
    ): pass