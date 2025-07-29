from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general.organization_role import MaleoIdentityOrganizationRoleGeneralSchemas
from maleo_identity.models.schemas.parameters.organization_role import MaleoIdentityOrganizationRoleParametersSchemas

class MaleoIdentityOrganizationRoleGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class GetSingle(
        MaleoIdentityOrganizationRoleGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        MaleoIdentityOrganizationRoleParametersSchemas.Base
    ): pass