from enum import Enum


class NewGroupDescMappingDiscriminator(str, Enum):
    IDENTIFIER = "identifier"
    LABEL = "label"

    def __str__(self) -> str:
        return str(self.value)
