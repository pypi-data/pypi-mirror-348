from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general.user_organization import MaleoIdentityUserOrganizationGeneralSchemas

class MaleoIdentityUserOrganizationServiceParametersTransfers:
    class GetMultipleFromUserQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultiple(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass