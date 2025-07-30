from __future__ import annotations
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.organization import MaleoIdentityOrganizationResultsSchemas

class MaleoIdentityOrganizationRepositoryResultsTransfers:
    class Row(
        MaleoIdentityOrganizationResultsSchemas.Query,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityOrganizationRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityOrganizationRepositoryResultsTransfers.Row]