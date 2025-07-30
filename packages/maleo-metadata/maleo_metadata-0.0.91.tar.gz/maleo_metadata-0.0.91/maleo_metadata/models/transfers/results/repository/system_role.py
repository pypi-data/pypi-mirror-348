from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.schemas.system_role import MaleoMetadataSystemRoleSchemas

class MaleoMetadataSystemRoleRepositoryResultsTransfers:
    class Row(
        MaleoMetadataSystemRoleSchemas.Name,
        MaleoMetadataSystemRoleSchemas.Key,
        BaseGeneralSchemas.Order,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoMetadataSystemRoleRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[MaleoMetadataSystemRoleRepositoryResultsTransfers.Row]