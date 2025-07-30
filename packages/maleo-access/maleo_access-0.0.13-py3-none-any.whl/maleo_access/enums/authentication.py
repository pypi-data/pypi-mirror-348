from enum import StrEnum

class MaleoAccessAuthenticationEnums:
    class IdentifierType(StrEnum):
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"