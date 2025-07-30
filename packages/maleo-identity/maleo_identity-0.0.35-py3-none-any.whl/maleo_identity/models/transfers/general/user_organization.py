from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.results.user_organization import MaleoIdentityUserOrganizationResultsSchemas
from maleo_identity.models.transfers.general.organization import OptionalExpandedOrganization
from maleo_identity.models.transfers.general.user import OptionalExpandedUser

class UserOrganizationTransfers(
    OptionalExpandedOrganization,
    OptionalExpandedUser,
    MaleoIdentityUserOrganizationResultsSchemas.Base,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass