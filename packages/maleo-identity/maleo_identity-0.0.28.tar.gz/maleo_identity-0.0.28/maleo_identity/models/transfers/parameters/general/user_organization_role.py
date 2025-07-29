from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralSchemas
from maleo_identity.models.schemas.parameters.user_organization_role import MaleoIdentityUserOrganizationRoleParametersSchemas

class MaleoIdentityUserOrganizationRoleGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class GetSingle(
        MaleoIdentityUserOrganizationRoleGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        MaleoIdentityUserOrganizationRoleParametersSchemas.Base
    ): pass