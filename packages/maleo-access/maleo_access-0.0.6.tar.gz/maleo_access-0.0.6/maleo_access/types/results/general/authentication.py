from typing import Union
from maleo_access.models.transfers.results.general.authentication import MaleoAccessAuthenticationGeneralResultsTransfers

class MaleoAccessAuthenticationGeneralResultsTypes:
    GenerateLoginTokens = Union[
        MaleoAccessAuthenticationGeneralResultsTransfers.Fail,
        MaleoAccessAuthenticationGeneralResultsTransfers.GenerateLoginTokens
    ]

    Login = Union[
        MaleoAccessAuthenticationGeneralResultsTransfers.Fail,
        MaleoAccessAuthenticationGeneralResultsTransfers.Login
    ]

    Logout = Union[
        MaleoAccessAuthenticationGeneralResultsTransfers.Fail,
        MaleoAccessAuthenticationGeneralResultsTransfers.Logout
    ]

    GenerateToken = Union[
        MaleoAccessAuthenticationGeneralResultsTransfers.Fail,
        MaleoAccessAuthenticationGeneralResultsTransfers.GenerateToken
    ]