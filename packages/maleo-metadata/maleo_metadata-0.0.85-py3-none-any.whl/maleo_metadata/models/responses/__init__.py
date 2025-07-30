from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeResponses
from .gender import MaleoMetadataGenderResponses
from .organization_type import MaleoMetadataOrganizationTypeResponses
from .service import MaleoMetadataServiceResponses
from .system_role import MaleoMetadataSystemRoleResponses
from .user_type import MaleoMetadataUserTypeResponses

class MaleoMetadataResponses:
    BloodType = MaleoMetadataBloodTypeResponses
    Gender = MaleoMetadataGenderResponses
    OrganizationType = MaleoMetadataOrganizationTypeResponses
    Service = MaleoMetadataServiceResponses
    SystemRole = MaleoMetadataSystemRoleResponses
    UserType = MaleoMetadataUserTypeResponses