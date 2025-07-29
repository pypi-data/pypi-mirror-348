from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers

class MaleoMetadataBloodTypeServiceParametersTransfers:
    class GetMultipleQuery(
        BaseServiceParametersTransfers.GetUnpaginatedMultipleQuery,
        BaseGeneralSchemas.Names,
        BaseGeneralSchemas.Keys,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultiple(
        BaseServiceParametersTransfers.GetUnpaginatedMultiple,
        BaseGeneralSchemas.Names,
        BaseGeneralSchemas.Keys,
        BaseGeneralSchemas.Uuids,
        BaseGeneralSchemas.Ids
    ): pass