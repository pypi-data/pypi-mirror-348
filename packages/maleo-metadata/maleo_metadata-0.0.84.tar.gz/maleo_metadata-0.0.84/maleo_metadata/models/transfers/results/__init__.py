from __future__ import annotations
from .client import MaleoMetadataClientResultsTransfers
from .general import MaleoMetadataGeneralResultsTransfers
from .query import MaleoMetadataQueryResultsTransfers

class MaleoMetadataResultsTransfers:
    Client = MaleoMetadataClientResultsTransfers
    General = MaleoMetadataGeneralResultsTransfers
    Query = MaleoMetadataQueryResultsTransfers