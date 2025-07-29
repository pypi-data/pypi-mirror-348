from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.parameters.organization import MaleoIdentityOrganizationParametersSchemas
from maleo_identity.models.schemas.general.organization import MaleoIdentityOrganizationGeneralSchemas

class MaleoIdentityOrganizationGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class GetSingle(
        MaleoIdentityOrganizationGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        BaseGeneralSchemas.IdentifierValue,
        MaleoIdentityOrganizationGeneralSchemas.IdentifierType
    ): pass

    class CreateOrUpdateQuery(MaleoIdentityOrganizationGeneralSchemas.Expand): pass

    class CreateOrUpdateData(MaleoIdentityOrganizationParametersSchemas.Base): pass

    class Create(CreateOrUpdateData, CreateOrUpdateQuery): pass

    class Update(
        CreateOrUpdateData,
        CreateOrUpdateQuery,
        BaseGeneralSchemas.IdentifierValue,
        MaleoIdentityOrganizationGeneralSchemas.IdentifierType
    ): pass