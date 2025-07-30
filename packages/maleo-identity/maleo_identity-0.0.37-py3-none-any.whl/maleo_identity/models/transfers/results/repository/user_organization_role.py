from __future__ import annotations
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.schemas.results.user_organization_role import MaleoIdentityUserOrganizationRoleResultsSchemas

class MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers:
    class Row(
        MaleoIdentityUserOrganizationRoleResultsSchemas.Base,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.Row]