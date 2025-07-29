from __future__ import annotations
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.user_organization import MaleoIdentityUserOrganizationResultsSchemas

class MaleoIdentityUserOrganizationQueryResultsTransfers:
    class Row(
        MaleoIdentityUserOrganizationResultsSchemas.Base,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityUserOrganizationQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserOrganizationQueryResultsTransfers.Row]