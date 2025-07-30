from enum import Enum


class SimpleGroupDescMappingDiscriminator(str, Enum):
    IDENTIFIER = "identifier"
    LABEL = "label"

    def __str__(self) -> str:
        return str(self.value)
