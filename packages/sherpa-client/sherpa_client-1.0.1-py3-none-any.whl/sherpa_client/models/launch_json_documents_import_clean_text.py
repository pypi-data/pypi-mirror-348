from enum import Enum


class LaunchJsonDocumentsImportCleanText(str, Enum):
    DEFAULT = "default"
    FALSE = "false"
    TRUE = "true"

    def __str__(self) -> str:
        return str(self.value)
