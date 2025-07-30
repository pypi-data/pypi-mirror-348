from __future__ import annotations
from .tables import MaleoIdentityTables
from .transfers import MaleoIdentityTransfers
from .responses import MaleoIdentityResponses

class MaleoIdentityModels:
    Tables = MaleoIdentityTables
    Transfers = MaleoIdentityTransfers
    Responses = MaleoIdentityResponses