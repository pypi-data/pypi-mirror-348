from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.schemas.organization_type import MaleoMetadataOrganizationTypeSchemas

class MaleoMetadataOrganizationTypeRepositoryResultsTransfers:
    class Row(
        MaleoMetadataOrganizationTypeSchemas.Name,
        MaleoMetadataOrganizationTypeSchemas.Key,
        BaseGeneralSchemas.Order,
        BaseServiceRepositoryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MaleoMetadataOrganizationTypeRepositoryResultsTransfers.Row

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[MaleoMetadataOrganizationTypeRepositoryResultsTransfers.Row]