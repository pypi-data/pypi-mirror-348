from enum import Enum


class AnnotationPatchStatus(str, Enum):
    KO = "KO"
    OK = "OK"

    def __str__(self) -> str:
        return str(self.value)
