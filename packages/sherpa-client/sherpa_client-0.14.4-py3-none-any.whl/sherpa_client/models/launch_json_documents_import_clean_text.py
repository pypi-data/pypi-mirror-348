from enum import Enum


class LaunchJsonDocumentsImportCleanText(str, Enum):
    TRUE = "true"
    FALSE = "false"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
