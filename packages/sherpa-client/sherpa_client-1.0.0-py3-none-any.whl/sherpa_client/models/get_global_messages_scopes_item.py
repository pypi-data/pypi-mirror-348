from enum import Enum


class GetGlobalMessagesScopesItem(str, Enum):
    LOGIN = "login"

    def __str__(self) -> str:
        return str(self.value)
