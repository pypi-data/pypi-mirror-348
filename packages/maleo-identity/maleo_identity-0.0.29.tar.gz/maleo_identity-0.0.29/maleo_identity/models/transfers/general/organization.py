from pydantic import BaseModel, Field
from typing import Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.results.organization import MaleoIdentityOrganizationResultsSchemas

#! Do not use this class, use the inherited class
class BaseOrganizationTransfers(
    MaleoIdentityOrganizationResultsSchemas.General,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass

class OrganizationTransfers(
    MaleoIdentityOrganizationResultsSchemas.General,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass

class OptionalExpandedOrganization(BaseModel):
    organization_details:Optional[OrganizationTransfers] = Field(None, description="Organization's details")