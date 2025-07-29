from __future__ import annotations
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers
from maleo_identity.models.schemas.results.user_system_role import MaleoIdentityUserSystemRoleResultsSchemas

class MaleoIdentityUserSystemRoleQueryResultsTransfers:
    class Row(
        MaleoIdentityUserSystemRoleResultsSchemas.Base,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoIdentityUserSystemRoleQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserSystemRoleQueryResultsTransfers.Row]