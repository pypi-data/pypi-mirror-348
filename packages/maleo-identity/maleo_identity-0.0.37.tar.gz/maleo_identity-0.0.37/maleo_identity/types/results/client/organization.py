from typing import Union
from maleo_identity.models.transfers.results.client.organization import MaleoIdentityOrganizationClientResultsTransfers

class MaleoIdentityOrganizationClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.NoData,
        MaleoIdentityOrganizationClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.SingleData
    ]