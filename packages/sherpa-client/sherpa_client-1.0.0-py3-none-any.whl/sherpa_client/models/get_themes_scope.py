from enum import Enum


class GetThemesScope(str, Enum):
    GROUP = "group"
    PLATFORM = "platform"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
