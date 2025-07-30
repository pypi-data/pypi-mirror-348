from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.schemas.user_type import MaleoMetadataUserTypeSchemas

class MaleoMetadataUserTypeRepositoryResultsTransfers:
    class Row(
        MaleoMetadataUserTypeSchemas.Name,
        MaleoMetadataUserTypeSchemas.Key,
        BaseGeneralSchemas.Order,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoMetadataUserTypeRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[MaleoMetadataUserTypeRepositoryResultsTransfers.Row]