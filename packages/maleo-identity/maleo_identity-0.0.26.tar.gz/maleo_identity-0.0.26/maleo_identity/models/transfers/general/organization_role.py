from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas
from maleo_identity.models.transfers.general.organization import OptionalExpandedOrganization

class OrganizationRoleTransfers(
    MaleoIdentityOrganizationRoleGeneralSchemas.Name,
    MaleoIdentityOrganizationRoleGeneralSchemas.Key,
    MaleoIdentityOrganizationRoleGeneralSchemas.Order,
    MaleoIdentityOrganizationRoleGeneralSchemas.IsDefault,
    OptionalExpandedOrganization,
    MaleoIdentityOrganizationRoleGeneralSchemas.OrganizationId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass