from typing import Union
from maleo_identity.models.transfers.results.repository.organization import MaleoIdentityOrganizationRepositoryResultsTransfers

class MaleoIdentityOrganizationRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationRepositoryResultsTransfers.Fail,
        MaleoIdentityOrganizationRepositoryResultsTransfers.NoData,
        MaleoIdentityOrganizationRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationRepositoryResultsTransfers.Fail,
        MaleoIdentityOrganizationRepositoryResultsTransfers.NoData,
        MaleoIdentityOrganizationRepositoryResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityOrganizationRepositoryResultsTransfers.Fail,
        MaleoIdentityOrganizationRepositoryResultsTransfers.SingleData
    ]