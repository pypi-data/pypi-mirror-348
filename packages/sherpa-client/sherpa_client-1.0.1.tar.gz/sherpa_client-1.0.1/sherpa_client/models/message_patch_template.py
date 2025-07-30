from enum import Enum


class MessagePatchTemplate(str, Enum):
    THYMELEAF = "thymeleaf"

    def __str__(self) -> str:
        return str(self.value)
