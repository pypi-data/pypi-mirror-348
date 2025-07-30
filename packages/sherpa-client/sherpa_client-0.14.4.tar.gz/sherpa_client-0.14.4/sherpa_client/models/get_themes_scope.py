from enum import Enum


class GetThemesScope(str, Enum):
    PLATFORM = "platform"
    GROUP = "group"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
