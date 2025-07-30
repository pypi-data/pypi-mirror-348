from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general.user_organization import MaleoIdentityUserOrganizationGeneralSchemas

class MaleoIdentityUserOrganizationClientParametersTransfers:
    class GetMultipleFromUser(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.UserId
    ): pass

    class GetMultipleFromOrganization(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultipleFromUserQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId
    ): pass