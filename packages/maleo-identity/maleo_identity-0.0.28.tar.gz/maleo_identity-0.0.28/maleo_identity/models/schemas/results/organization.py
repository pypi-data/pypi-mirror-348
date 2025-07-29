from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.general.organization import MaleoIdentityOrganizationGeneralSchemas

class MaleoIdentityOrganizationResultsSchemas:
    class General(
        MaleoIdentityOrganizationGeneralSchemas.Name,
        MaleoIdentityOrganizationGeneralSchemas.Key,
        MaleoIdentityOrganizationGeneralSchemas.OptionalParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalExpandedOrganizationType,
        MaleoMetadataOrganizationTypeExpandedSchemas.SimpleOrganizationType
    ): pass

    class Query(
        MaleoIdentityOrganizationGeneralSchemas.Name,
        MaleoIdentityOrganizationGeneralSchemas.Key,
        MaleoIdentityOrganizationGeneralSchemas.OptionalParentOrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.SimpleOrganizationType
    ): pass