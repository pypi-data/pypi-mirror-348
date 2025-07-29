from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeQueryResultsTypes
from .gender import MaleoMetadataGenderQueryResultsTypes
from .organization_type import MaleoMetadataOrganizationTypeQueryResultsTypes
from .service import MaleoMetadataServiceQueryResultsTypes
from .system_role import MaleoMetadataSystemRoleQueryResultsTypes
from .user_type import MaleoMetadataUserTypeQueryResultsTypes

class MaleoMetadataQueryResultsTypes:
    BloodType = MaleoMetadataBloodTypeQueryResultsTypes
    Gender = MaleoMetadataGenderQueryResultsTypes
    OrganizationType = MaleoMetadataOrganizationTypeQueryResultsTypes
    Service = MaleoMetadataServiceQueryResultsTypes
    SystemRole = MaleoMetadataSystemRoleQueryResultsTypes
    UserType = MaleoMetadataUserTypeQueryResultsTypes