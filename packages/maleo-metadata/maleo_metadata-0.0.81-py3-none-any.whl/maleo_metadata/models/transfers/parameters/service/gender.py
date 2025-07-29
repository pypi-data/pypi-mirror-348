from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers

class MaleoMetadataGenderServiceParametersTransfers:
    class GetMultipleQuery(
        BaseServiceParametersTransfers.GetUnpaginatedMultipleQuery,
        BaseGeneralSchemas.Ids
    ): pass

    class GetMultiple(
        BaseServiceParametersTransfers.GetUnpaginatedMultiple,
        BaseGeneralSchemas.Ids
    ): pass