from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas

class MaleoIdentityOrganizationRoleParametersSchemas:
    class Base(
        MaleoIdentityOrganizationRoleGeneralSchemas.Key,
        MaleoIdentityOrganizationRoleGeneralSchemas.OrganizationId
    ): pass