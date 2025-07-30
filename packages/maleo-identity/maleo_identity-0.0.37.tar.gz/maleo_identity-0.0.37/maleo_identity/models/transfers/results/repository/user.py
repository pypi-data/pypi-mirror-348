from __future__ import annotations
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.user import MaleoIdentityUserResultsSchemas

class MaleoIdentityUserRepositoryResultsTransfers:
    class Row(
        MaleoIdentityUserResultsSchemas.Query,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityUserRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserRepositoryResultsTransfers.Row]

    class PasswordRow(
        MaleoIdentityUserResultsSchemas.PasswordQuery,
        BaseResultSchemas.BaseRow
    ): pass

    class SinglePassword(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityUserRepositoryResultsTransfers.PasswordRow