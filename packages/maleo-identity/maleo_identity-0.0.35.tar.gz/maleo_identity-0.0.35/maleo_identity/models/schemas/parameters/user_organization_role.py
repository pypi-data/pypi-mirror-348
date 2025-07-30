from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas

class MaleoIdentityUserOrganizationRoleParametersSchemas:
    class Base(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Key,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.UserId
    ): pass