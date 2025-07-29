from typing import Union
from maleo_identity.models.transfers.results.query.user_profile import MaleoIdentityUserProfileQueryResultsTransfers

class MaleoIdentityUserProfileQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserProfileQueryResultsTransfers.Fail,
        MaleoIdentityUserProfileQueryResultsTransfers.NoData,
        MaleoIdentityUserProfileQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserProfileQueryResultsTransfers.Fail,
        MaleoIdentityUserProfileQueryResultsTransfers.NoData,
        MaleoIdentityUserProfileQueryResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserProfileQueryResultsTransfers.Fail,
        MaleoIdentityUserProfileQueryResultsTransfers.SingleData
    ]