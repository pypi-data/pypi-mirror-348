from typing import Union
from maleo_identity.models.transfers.results.query.user_organization_role import MaleoIdentityUserOrganizationRoleQueryResultsTransfers

class MaleoIdentityUserOrganizationRoleQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationRoleQueryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleQueryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationRoleQueryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleQueryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleQueryResultsTransfers.SingleData
    ]