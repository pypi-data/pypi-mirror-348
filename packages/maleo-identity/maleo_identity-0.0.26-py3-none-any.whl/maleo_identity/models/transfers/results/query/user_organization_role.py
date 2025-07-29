from __future__ import annotations
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.user_organization_role import MaleoIdentityUserOrganizationRoleResultsSchemas

class MaleoIdentityUserOrganizationRoleQueryResultsTransfers:
    class Row(
        MaleoIdentityUserOrganizationRoleResultsSchemas.Base,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityUserOrganizationRoleQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserOrganizationRoleQueryResultsTransfers.Row]