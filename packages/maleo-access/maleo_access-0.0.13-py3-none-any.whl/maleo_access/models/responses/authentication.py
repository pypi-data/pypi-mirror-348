from __future__ import annotations
from maleo_foundation.models.responses import BaseResponses
from maleo_access.models.transfers.general.authentication import MaleoAccessAuthenticationGeneralTransfers

class MaleoAccessAuthenticationResponses:
    #* ----- ----- Response ----- ----- *#
    class Fail(BaseResponses.Fail):
        code:str = "ACC-ATH-001"
        message:str = "Authentication Failed"
        description:str = "External error: Authentication failed"
        other:str = "Ensure parameter(s) are correct"

    class InvalidCredentials(BaseResponses.Fail):
        code:str = "ACC-ATH-002"
        message:str = "Authentication Failed"
        description:str = "External error: Invalid credentials"
        other:str = "Ensure parameter(s) are correct"

    class Login(BaseResponses.SingleData):
        code:str = "ACC-ATH-003"
        message:str = "Login Successful"
        description:str = "Login attempt is successful"
        data:MaleoAccessAuthenticationGeneralTransfers.LoginData

    class Logout(BaseResponses.NoData):
        code:str = "ACC-ATH-004"
        message:str = "Logout Successful"
        description:str = "Logout attempt is successful"

    class GenerateToken(BaseResponses.SingleData):
        code:str = "ACC-ATH-005"
        message:str = "Token generation successful"
        description:str = "Succesfully generated token based on given data"
        data:MaleoAccessAuthenticationGeneralTransfers.Token