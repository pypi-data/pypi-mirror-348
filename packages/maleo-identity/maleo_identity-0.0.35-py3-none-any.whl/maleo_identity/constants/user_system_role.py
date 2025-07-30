from typing import Dict, List
from maleo_identity.enums.user import MaleoIdentityUserEnums
from maleo_identity.enums.user_system_role import MaleoIdentityUserSystemRoleEnums

class MaleoIdentityUserSystemRoleConstants:
    EXPANDABLE_FIELDS_DEPENDENCIES_MAP:Dict[
        MaleoIdentityUserSystemRoleEnums.ExpandableFields,
        List[MaleoIdentityUserSystemRoleEnums.ExpandableFields]
    ] = {
        MaleoIdentityUserSystemRoleEnums.ExpandableFields.USER: [
            MaleoIdentityUserSystemRoleEnums.ExpandableFields.USER_TYPE
        ]
    }

    USER_EXPANDABLE_FIELDS_MAP:Dict[
        MaleoIdentityUserSystemRoleEnums.ExpandableFields,
        MaleoIdentityUserEnums.ExpandableFields
    ] = {
        MaleoIdentityUserSystemRoleEnums.ExpandableFields.USER_TYPE: MaleoIdentityUserEnums.ExpandableFields.USER_TYPE
    }