from __future__ import annotations
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.user import MaleoIdentityUserResultsSchemas

class MaleoIdentityUserQueryResultsTransfers:
    class Row(
        MaleoIdentityUserResultsSchemas.Query,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityUserQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserQueryResultsTransfers.Row]

    class PasswordRow(
        MaleoIdentityUserResultsSchemas.PasswordQuery,
        BaseResultSchemas.BaseRow
    ): pass

    class SinglePassword(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityUserQueryResultsTransfers.PasswordRow