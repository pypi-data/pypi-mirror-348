from __future__ import annotations
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.general.organization import MaleoIdentityOrganizationGeneralSchemas

class MaleoIdentityOrganizationServiceParametersTransfers:
    class GetMultipleQuery(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseGeneralSchemas.Keys,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultiple(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        BaseGeneralSchemas.Keys,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass