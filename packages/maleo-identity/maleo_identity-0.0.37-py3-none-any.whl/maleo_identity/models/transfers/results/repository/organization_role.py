from __future__ import annotations
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.organization_role import MaleoIdentityOrganizationRoleResultsSchemas

class MaleoIdentityOrganizationRoleRepositoryResultsTransfers:
    class Row(
        MaleoIdentityOrganizationRoleResultsSchemas.Base,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityOrganizationRoleRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityOrganizationRoleRepositoryResultsTransfers.Row]