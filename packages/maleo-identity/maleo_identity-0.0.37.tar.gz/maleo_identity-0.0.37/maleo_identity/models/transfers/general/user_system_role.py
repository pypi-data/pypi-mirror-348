from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.results.user_system_role import MaleoIdentityUserSystemRoleResultsSchemas
from maleo_identity.models.transfers.general.user import OptionalExpandedUser

class UserSystemRoleTransfers(
    MaleoMetadataSystemRoleExpandedSchemas.OptionalExpandedSystemRole,
    OptionalExpandedUser,
    MaleoIdentityUserSystemRoleResultsSchemas.Base,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass