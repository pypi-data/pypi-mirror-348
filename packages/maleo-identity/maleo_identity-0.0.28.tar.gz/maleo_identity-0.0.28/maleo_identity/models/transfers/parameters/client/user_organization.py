from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general.user_organization import MaleoIdentityUserOrganizationGeneralSchemas

class MaleoIdentityUserOrganizationClientParametersTransfers:
    class GetMultipleFromUser(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.UserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleFromOrganization(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleFromUserQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfOrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.OptionalListOfUserId,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass