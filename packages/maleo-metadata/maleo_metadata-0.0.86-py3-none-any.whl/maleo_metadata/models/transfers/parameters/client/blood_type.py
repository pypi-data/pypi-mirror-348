from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers

class MaleoMetadataBloodTypeClientParametersTransfers:
    class GetMultiple(
        BaseClientParametersTransfers.GetUnpaginatedMultiple,
        BaseGeneralSchemas.Names,
        BaseGeneralSchemas.Keys,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultipleQuery(
        BaseClientParametersTransfers.GetUnpaginatedMultipleQuery,
        BaseGeneralSchemas.Names,
        BaseGeneralSchemas.Keys,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass