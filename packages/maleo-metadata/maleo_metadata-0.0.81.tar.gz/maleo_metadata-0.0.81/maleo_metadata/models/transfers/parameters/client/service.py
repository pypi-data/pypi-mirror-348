from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers

class MaleoMetadataServiceClientParametersTransfers:
    class GetMultiple(
        BaseClientParametersTransfers.GetUnpaginatedMultiple,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultipleQuery(
        BaseClientParametersTransfers.GetUnpaginatedMultipleQuery,
        BaseGeneralSchemas.Ids
    ): pass