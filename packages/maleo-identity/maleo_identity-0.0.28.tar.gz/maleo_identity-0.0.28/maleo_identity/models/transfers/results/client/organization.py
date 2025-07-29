from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_identity.models.transfers.general.organization import OrganizationTransfers

class MaleoIdentityOrganizationClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:OrganizationTransfers = Field(..., description="Single organization data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[OrganizationTransfers] = Field(..., description="Multiple organizations data")