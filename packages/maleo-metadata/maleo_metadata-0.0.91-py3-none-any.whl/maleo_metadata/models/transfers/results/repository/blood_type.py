from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.schemas.blood_type import MaleoMetadataBloodTypeSchemas

class MaleoMetadataBloodTypeRepositoryResultsTransfers:
    class Row(
        MaleoMetadataBloodTypeSchemas.Name,
        MaleoMetadataBloodTypeSchemas.Key,
        BaseGeneralSchemas.Order,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoMetadataBloodTypeRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[MaleoMetadataBloodTypeRepositoryResultsTransfers.Row]