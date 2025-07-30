from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas
from maleo_identity.models.transfers.general.organization import OptionalExpandedOrganization
from maleo_identity.models.transfers.general.user import OptionalExpandedUser

class UserOrganizationRoleTransfers(
    MaleoIdentityUserOrganizationRoleGeneralSchemas.Name,
    MaleoIdentityUserOrganizationRoleGeneralSchemas.Key,
    MaleoIdentityUserOrganizationRoleGeneralSchemas.Order,
    MaleoIdentityUserOrganizationRoleGeneralSchemas.IsDefault,
    OptionalExpandedOrganization,
    MaleoIdentityUserOrganizationRoleGeneralSchemas.OrganizationId,
    OptionalExpandedUser,
    MaleoIdentityUserOrganizationRoleGeneralSchemas.UserId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass