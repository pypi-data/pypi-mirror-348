from typing import Union
from maleo_identity.models.transfers.results.query.organization_role import MaleoIdentityOrganizationRoleQueryResultsTransfers

class MaleoIdentityOrganizationRoleQueryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationRoleQueryResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleQueryResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleQueryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationRoleQueryResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleQueryResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleQueryResultsTransfers.SingleData
    ]