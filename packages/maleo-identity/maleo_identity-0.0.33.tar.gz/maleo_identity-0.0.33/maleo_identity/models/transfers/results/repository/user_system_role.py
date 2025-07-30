from __future__ import annotations
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.user_system_role import MaleoIdentityUserSystemRoleResultsSchemas

class MaleoIdentityUserSystemRoleRepositoryResultsTransfers:
    class Row(
        MaleoIdentityUserSystemRoleResultsSchemas.Base,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityUserSystemRoleRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserSystemRoleRepositoryResultsTransfers.Row]