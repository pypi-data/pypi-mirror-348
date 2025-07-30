from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.enums.organization import MaleoIdentityOrganizationEnums
from maleo_identity.models.transfers.general.organization import OrganizationTransfers

class MaleoIdentityOrganizationResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "IDT-ORG-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoIdentityOrganizationEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "IDT-ORG-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-ORG-003"
        message:str = "Organization found"
        description:str = "Requested organization found in database"
        data:OrganizationTransfers = Field(..., description="Organization")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-ORG-004"
        message:str = "Organizations found"
        description:str = "Requested organizations found in database"
        data:list[OrganizationTransfers] = Field(..., description="Organizations")

    class CreateFailed(BaseResponses.BadRequest):
        code:str = "IDT-ORG-005"
        message:str = "Failed creating new organization"

    class CreateSuccess(BaseResponses.SingleData):
        code:str = "IDT-ORG-006"
        message:str = "Successfully created new organization"
        data:OrganizationTransfers = Field(..., description="Organization")

    class UpdateFailed(BaseResponses.BadRequest):
        code:str = "IDT-ORG-007"
        message:str = "Failed updating organization's data"

    class UpdateSuccess(BaseResponses.SingleData):
        code:str = "IDT-ORG-008"
        message:str = "Successfully updated organization's data"
        data:OrganizationTransfers = Field(..., description="Organization")