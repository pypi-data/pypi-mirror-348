from enum import Enum


class VectorParamsNativeRRF(str, Enum):
    IF_AVAILABLE = "if_available"
    NO = "no"
    YES = "yes"

    def __str__(self) -> str:
        return str(self.value)
