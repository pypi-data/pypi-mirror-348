from enum import Enum


class VectorParamsNativeRRF(str, Enum):
    YES = "yes"
    NO = "no"
    IF_AVAILABLE = "if_available"

    def __str__(self) -> str:
        return str(self.value)
