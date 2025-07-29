from enum import Enum


class FindSimilarSegmentsSearchType(str, Enum):
    HYBRID = "hybrid"
    TEXT = "text"
    VECTOR = "vector"

    def __str__(self) -> str:
        return str(self.value)
