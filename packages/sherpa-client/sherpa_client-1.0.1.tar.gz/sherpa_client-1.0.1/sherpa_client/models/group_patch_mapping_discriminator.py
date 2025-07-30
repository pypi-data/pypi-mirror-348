from enum import Enum


class GroupPatchMappingDiscriminator(str, Enum):
    IDENTIFIER = "identifier"
    LABEL = "label"

    def __str__(self) -> str:
        return str(self.value)
