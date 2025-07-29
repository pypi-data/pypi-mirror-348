from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_access.enums.authentication import MaleoAccessAuthenticationEnums

class MaleoAccessAuthenticationGeneralParametersTransfers:
    class Login(BaseModel):
        system_role:MaleoMetadataSystemRoleEnums.SystemRole = Field(..., description="System role")
        organization_key:Optional[str] = Field(..., description="Organization's Key")
        identifier_type:MaleoAccessAuthenticationEnums.IdentifierType = Field(..., description="Identifier's type")
        identifier_value:str = Field(..., description="Identifier's value")
        password:str = Field(..., description="Password")

    class Base(BaseModel):
        system_role:MaleoMetadataSystemRoleEnums.SystemRole = Field(..., description="System role")
        organization_key:Optional[str] = Field(..., description="Organization's Key")
        identifier_type:MaleoAccessAuthenticationEnums.IdentifierType = Field(..., description="Identifier's type")
        identifier_value:str = Field(..., description="Identifier's value")
        password:str = Field(..., description="Password")