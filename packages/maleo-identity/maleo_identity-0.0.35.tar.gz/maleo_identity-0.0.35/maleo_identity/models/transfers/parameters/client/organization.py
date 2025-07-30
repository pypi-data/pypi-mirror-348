from __future__ import annotations
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.general.organization import MaleoIdentityOrganizationGeneralSchemas

class MaleoIdentityOrganizationClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseGeneralSchemas.Keys,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseGeneralSchemas.Keys,
        MaleoIdentityOrganizationGeneralSchemas.OptionalListOfParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationType,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass