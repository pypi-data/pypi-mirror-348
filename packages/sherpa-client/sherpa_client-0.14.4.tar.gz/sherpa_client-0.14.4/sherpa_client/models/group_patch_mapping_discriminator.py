from enum import Enum


class GroupPatchMappingDiscriminator(str, Enum):
    LABEL = "label"
    IDENTIFIER = "identifier"

    def __str__(self) -> str:
        return str(self.value)
