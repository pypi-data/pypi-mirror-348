from enum import Enum


class GetFavoriteThemeScope(str, Enum):
    PLATFORM = "platform"
    GROUP = "group"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
