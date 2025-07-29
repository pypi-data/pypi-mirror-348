from typing import Union
from maleo_identity.models.transfers.results.query.user_system_role import MaleoIdentityUserSystemRoleQueryResultsTransfers

class MaleoIdentityUserSystemRoleQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserSystemRoleQueryResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleQueryResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserSystemRoleQueryResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleQueryResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleQueryResultsTransfers.SingleData
    ]

    Create = Union[
        MaleoIdentityUserSystemRoleQueryResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleQueryResultsTransfers.SingleData
    ]