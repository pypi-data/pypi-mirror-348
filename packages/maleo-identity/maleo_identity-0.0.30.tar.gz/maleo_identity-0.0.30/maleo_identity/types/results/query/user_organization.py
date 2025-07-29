from typing import Union
from maleo_identity.models.transfers.results.query.user_organization import MaleoIdentityUserOrganizationQueryResultsTransfers

class MaleoIdentityUserOrganizationQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationQueryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationQueryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationQueryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationQueryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationQueryResultsTransfers.SingleData
    ]

    Create = Union[
        MaleoIdentityUserOrganizationQueryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationQueryResultsTransfers.SingleData
    ]