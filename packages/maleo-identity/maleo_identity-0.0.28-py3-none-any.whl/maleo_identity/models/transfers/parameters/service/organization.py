from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.general.organization import MaleoIdentityOrganizationGeneralSchemas

class MaleoIdentityOrganizationServiceParametersTransfers:
    class GetMultipleQuery(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery
    ): pass

    class GetMultiple(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseServiceParametersTransfers.GetPaginatedMultiple
    ): pass