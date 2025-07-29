from __future__ import annotations
from .client import MaleoIdentityClientResultsTransfers
from .general import MaleoIdentityGeneralResultsTransfers
from .query import MaleoIdentityQueryResultsTransfers

class MaleoIdentityResultsTransfers:
    Client = MaleoIdentityClientResultsTransfers
    General = MaleoIdentityGeneralResultsTransfers
    Query = MaleoIdentityQueryResultsTransfers