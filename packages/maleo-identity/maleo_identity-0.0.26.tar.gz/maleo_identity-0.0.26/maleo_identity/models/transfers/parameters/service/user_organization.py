from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general.user_organization import MaleoIdentityUserOrganizationGeneralSchemas

class MaleoIdentityUserOrganizationServiceParametersTransfers:
    class GetMultipleFromUserQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultiple(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseServiceParametersTransfers.GetPaginatedMultiple
    ): pass