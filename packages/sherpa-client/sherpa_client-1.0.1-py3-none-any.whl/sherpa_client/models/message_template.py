from enum import Enum


class MessageTemplate(str, Enum):
    THYMELEAF = "thymeleaf"

    def __str__(self) -> str:
        return str(self.value)
