from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas

class MaleoIdentityUserOrganizationRoleResultsSchemas:
    class Base(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Name,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Key,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Order,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.IsDefault,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationRoleGeneralSchemas.UserId
    ): pass