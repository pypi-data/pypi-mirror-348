from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general.user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas

class MaleoIdentityUserSystemRoleResultsSchemas:
    class Base(
        MaleoMetadataSystemRoleExpandedSchemas.SimpleSystemRole,
        MaleoIdentityUserSystemRoleGeneralSchemas.UserId
    ): pass