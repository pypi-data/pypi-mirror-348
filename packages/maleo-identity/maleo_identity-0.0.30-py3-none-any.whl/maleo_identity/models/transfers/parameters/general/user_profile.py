from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.parameters.user_profile import MaleoIdentityUserProfileParametersSchemas
from maleo_identity.models.schemas.general.user_profile import MaleoIdentityUserProfileGeneralSchemas

class MaleoIdentityUserProfileGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class GetSingle(
        MaleoIdentityUserProfileGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        BaseGeneralSchemas.IdentifierValue,
        MaleoIdentityUserProfileGeneralSchemas.IdentifierType
    ): pass

    class CreateOrUpdateQuery(MaleoIdentityUserProfileGeneralSchemas.Expand): pass

    class CreateOrUpdateBody(MaleoIdentityUserProfileParametersSchemas.Base): pass

    class CreateOrUpdateData(MaleoIdentityUserProfileParametersSchemas.Extended): pass

    class Create(
        CreateOrUpdateData,
        CreateOrUpdateQuery
    ): pass

    class Update(
        CreateOrUpdateData,
        CreateOrUpdateQuery,
        BaseGeneralSchemas.IdentifierValue,
        MaleoIdentityUserProfileGeneralSchemas.IdentifierType
    ): pass