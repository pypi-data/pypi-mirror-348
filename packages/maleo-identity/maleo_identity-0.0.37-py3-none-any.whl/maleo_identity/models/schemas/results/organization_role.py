from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas

class MaleoIdentityOrganizationRoleResultsSchemas:
    class Base(
        MaleoIdentityOrganizationRoleGeneralSchemas.Name,
        MaleoIdentityOrganizationRoleGeneralSchemas.Key,
        MaleoIdentityOrganizationRoleGeneralSchemas.Order,
        MaleoIdentityOrganizationRoleGeneralSchemas.IsDefault,
        MaleoIdentityOrganizationRoleGeneralSchemas.OrganizationId
    ): pass