from __future__ import annotations
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.user_profile import MaleoIdentityUserProfileResultsSchemas

class MaleoIdentityUserProfileRepositoryResultsTransfers:
    class Row(
        MaleoIdentityUserProfileResultsSchemas.Query,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityUserProfileRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserProfileRepositoryResultsTransfers.Row]