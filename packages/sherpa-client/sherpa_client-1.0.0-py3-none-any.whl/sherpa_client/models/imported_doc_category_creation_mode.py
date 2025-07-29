from enum import Enum


class ImportedDocCategoryCreationMode(str, Enum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    UNDEFINED = "undefined"

    def __str__(self) -> str:
        return str(self.value)
