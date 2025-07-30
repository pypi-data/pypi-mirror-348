from enum import Enum


class NewGroupDescMappingDiscriminator(str, Enum):
    LABEL = "label"
    IDENTIFIER = "identifier"

    def __str__(self) -> str:
        return str(self.value)
