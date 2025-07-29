from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.general.organization import MaleoIdentityOrganizationGeneralSchemas

class MaleoIdentityOrganizationClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseClientParametersTransfers.GetPaginatedMultiple
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery
    ): pass