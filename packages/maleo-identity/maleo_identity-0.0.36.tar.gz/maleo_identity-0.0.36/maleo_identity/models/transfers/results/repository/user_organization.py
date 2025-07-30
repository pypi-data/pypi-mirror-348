from __future__ import annotations
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.user_organization import MaleoIdentityUserOrganizationResultsSchemas

class MaleoIdentityUserOrganizationRepositoryResultsTransfers:
    class Row(
        MaleoIdentityUserOrganizationResultsSchemas.Base,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityUserOrganizationRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserOrganizationRepositoryResultsTransfers.Row]