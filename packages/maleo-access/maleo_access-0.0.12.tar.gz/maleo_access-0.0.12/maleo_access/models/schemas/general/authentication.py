from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoAccessAuthenticationGeneralSchemas:
    class Token(BaseModel):
        token:str = Field(..., description="Access Token")