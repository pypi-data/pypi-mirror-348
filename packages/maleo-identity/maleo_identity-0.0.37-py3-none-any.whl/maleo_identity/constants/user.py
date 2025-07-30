from typing import Dict, List
from uuid import UUID
from maleo_identity.enums.user import MaleoIdentityUserEnums
from maleo_identity.enums.user_profile import MaleoIdentityUserProfileEnums

class MaleoIdentityUserConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoIdentityUserEnums.IdentifierType,
        object
    ] = {
        MaleoIdentityUserEnums.IdentifierType.ID: int,
        MaleoIdentityUserEnums.IdentifierType.UUID: UUID,
        MaleoIdentityUserEnums.IdentifierType.USERNAME: str,
        MaleoIdentityUserEnums.IdentifierType.EMAIL: str,
        MaleoIdentityUserEnums.IdentifierType.PHONE: str
    }

    EXPANDABLE_FIELDS_DEPENDENCIES_MAP:Dict[
        MaleoIdentityUserEnums.ExpandableFields,
        List[MaleoIdentityUserEnums.ExpandableFields]
    ] = {
        MaleoIdentityUserEnums.ExpandableFields.PROFILE: [
            MaleoIdentityUserEnums.ExpandableFields.GENDER,
            MaleoIdentityUserEnums.ExpandableFields.BLOOD_TYPE
        ]
    }

    USER_PROFILE_EXPANDABLE_FIELDS_MAP:Dict[
        MaleoIdentityUserEnums.ExpandableFields,
        MaleoIdentityUserProfileEnums.ExpandableFields
    ] = {
        MaleoIdentityUserEnums.ExpandableFields.GENDER: MaleoIdentityUserProfileEnums.ExpandableFields.GENDER,
        MaleoIdentityUserEnums.ExpandableFields.BLOOD_TYPE: MaleoIdentityUserProfileEnums.ExpandableFields.BLOOD_TYPE
    }