from typing import Union
from maleo_identity.models.transfers.results.query.organization import MaleoIdentityOrganizationQueryResultsTransfers

class MaleoIdentityOrganizationQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationQueryResultsTransfers.Fail,
        MaleoIdentityOrganizationQueryResultsTransfers.NoData,
        MaleoIdentityOrganizationQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationQueryResultsTransfers.Fail,
        MaleoIdentityOrganizationQueryResultsTransfers.NoData,
        MaleoIdentityOrganizationQueryResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityOrganizationQueryResultsTransfers.Fail,
        MaleoIdentityOrganizationQueryResultsTransfers.SingleData
    ]