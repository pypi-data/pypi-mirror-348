from maleo_identity.models.schemas.general.user_organization import MaleoIdentityUserOrganizationGeneralSchemas

class MaleoIdentityUserOrganizationParametersSchemas:
    class Base(
        MaleoIdentityUserOrganizationGeneralSchemas.OrganizationId,
        MaleoIdentityUserOrganizationGeneralSchemas.UserId
    ): pass