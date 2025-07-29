from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeGeneralResultsTypes
from .gender import MaleoMetadataGenderGeneralResultsTypes
from .organization_type import MaleoMetadataOrganizationTypeGeneralResultsTypes
from .service import MaleoMetadataServiceGeneralResultsTypes
from .system_role import MaleoMetadataSystemRoleGeneralResultsTypes
from .user_type import MaleoMetadataUserTypeGeneralResultsTypes

class MaleoMetadataGeneralResultsTypes:
    BloodType = MaleoMetadataBloodTypeGeneralResultsTypes
    Gender = MaleoMetadataGenderGeneralResultsTypes
    OrganizationType = MaleoMetadataOrganizationTypeGeneralResultsTypes
    Service = MaleoMetadataServiceGeneralResultsTypes
    SystemRole = MaleoMetadataSystemRoleGeneralResultsTypes
    UserType = MaleoMetadataUserTypeGeneralResultsTypes