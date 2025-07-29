from __future__ import annotations
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.organization_role import MaleoIdentityOrganizationRoleResultsSchemas

class MaleoIdentityOrganizationRoleQueryResultsTransfers:
    class Row(
        MaleoIdentityOrganizationRoleResultsSchemas.Base,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityOrganizationRoleQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityOrganizationRoleQueryResultsTransfers.Row]