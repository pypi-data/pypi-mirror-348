from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.parameters.user import MaleoIdentityUserParametersSchemas
from maleo_identity.models.schemas.general.user import MaleoIdentityUserGeneralSchemas

class MaleoIdentityUserGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class BaseGetSingle(
        BaseGeneralSchemas.IdentifierValue,
        MaleoIdentityUserGeneralSchemas.IdentifierType
    ): pass

    class GetSinglePassword(BaseGetSingle): pass

    class GetSingle(
        MaleoIdentityUserGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        BaseGetSingle
    ): pass

    class CreateOrUpdateQuery(MaleoIdentityUserGeneralSchemas.Expand): pass

    class UpdateData(MaleoIdentityUserParametersSchemas.Base): pass

    class CreateData(MaleoIdentityUserParametersSchemas.Extended): pass

    class Update(
        CreateOrUpdateQuery,
        UpdateData,
        BaseGeneralSchemas.IdentifierValue,
        MaleoIdentityUserGeneralSchemas.IdentifierType
    ): pass

    class Create(
        CreateOrUpdateQuery,
        CreateData
    ): pass