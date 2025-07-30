from __future__ import annotations
from pydantic import BaseModel, Field, field_serializer, FieldSerializationInfo
from typing import Optional, Any
from uuid import UUID
from maleo_identity.models.transfers.general.user import UserTransfers
from maleo_access.models.schemas.general.authentication import MaleoAccessAuthenticationGeneralSchemas

class MaleoAccessAuthenticationGeneralTransfers:
    class BaseLoginData(BaseModel):
        system_role:UUID = Field(..., description="System role's UUID"),
        user:UUID = Field(..., description="user's UUID"),
        organization:Optional[UUID] = Field(None, description="Organization's UUID")
        organization_roles:Optional[list[UUID]] = Field(None, description="Organization Role's UUID")
        token:str = Field(..., description="Access Token")

        @field_serializer('*')
        def serialize_fields(self, value, info: FieldSerializationInfo) -> Any:
            """Recursively serialize UUIDs, datetimes, and dates in complex structures."""

            def serialize(v: Any) -> Any:
                if isinstance(v, UUID):
                    return str(v)
                if isinstance(v, list):
                    return [serialize(item) for item in v]
                if isinstance(v, tuple):
                    return tuple(serialize(item) for item in v)
                if isinstance(v, dict):
                    return {serialize(k): serialize(val) for k, val in v.items()}
                return v

            return serialize(value)

    class LoginTokens(BaseModel):
        refresh_token:str = Field(..., description="Refresh Token")
        access_token:str = Field(..., description="Access Token")

    class LoginData(BaseModel):
        base:MaleoAccessAuthenticationGeneralTransfers.BaseLoginData = Field(..., description="Base login data")
        user:UserTransfers = Field(..., description="User data")

    class Token(MaleoAccessAuthenticationGeneralSchemas.Token): pass