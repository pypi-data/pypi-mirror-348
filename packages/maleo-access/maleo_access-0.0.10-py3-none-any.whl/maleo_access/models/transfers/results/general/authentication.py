from __future__ import annotations
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_access.models.transfers.general.authentication import MaleoAccessAuthenticationGeneralTransfers

class MaleoAccessAuthenticationGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class GenerateLoginTokens(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoAccessAuthenticationGeneralTransfers.LoginTokens

    class Login(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoAccessAuthenticationGeneralTransfers.LoginData

    class Logout(BaseServiceGeneralResultsTransfers.NoData): pass

    class GenerateToken(BaseServiceGeneralResultsTransfers.SingleData):
        data:MaleoAccessAuthenticationGeneralTransfers.Token