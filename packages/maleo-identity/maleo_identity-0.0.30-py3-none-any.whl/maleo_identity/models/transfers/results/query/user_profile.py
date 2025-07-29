from __future__ import annotations
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.user_profile import MaleoIdentityUserProfileResultsSchemas

class MaleoIdentityUserProfileQueryResultsTransfers:
    class Row(
        MaleoIdentityUserProfileResultsSchemas.Query,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityUserProfileQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserProfileQueryResultsTransfers.Row]