from enum import Enum


class GroupDescMappingDiscriminator(str, Enum):
    IDENTIFIER = "identifier"
    LABEL = "label"

    def __str__(self) -> str:
        return str(self.value)
