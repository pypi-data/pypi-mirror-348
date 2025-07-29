from typing import Union
from maleo_identity.models.transfers.results.general.organization import MaleoIdentityOrganizationGeneralResultsTransfers

class MaleoIdentityOrganizationGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationGeneralResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.SingleData
    ]