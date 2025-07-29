from __future__ import annotations
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.organization import MaleoIdentityOrganizationResultsSchemas

class MaleoIdentityOrganizationQueryResultsTransfers:
    class Row(
        MaleoIdentityOrganizationResultsSchemas.Query,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityOrganizationQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityOrganizationQueryResultsTransfers.Row]