from typing import Union
from maleo_identity.models.transfers.results.query.user import MaleoIdentityUserQueryResultsTransfers

class MaleoIdentityUserQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserQueryResultsTransfers.Fail,
        MaleoIdentityUserQueryResultsTransfers.NoData,
        MaleoIdentityUserQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserQueryResultsTransfers.Fail,
        MaleoIdentityUserQueryResultsTransfers.NoData,
        MaleoIdentityUserQueryResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserQueryResultsTransfers.Fail,
        MaleoIdentityUserQueryResultsTransfers.SingleData
    ]

    GetSinglePassword = Union[
        MaleoIdentityUserQueryResultsTransfers.Fail,
        MaleoIdentityUserQueryResultsTransfers.SinglePassword
    ]