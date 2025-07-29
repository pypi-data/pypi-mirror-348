from enum import Enum


class SearchFilterFilterType(str, Enum):
    QUERY = "query"
    TERM = "term"

    def __str__(self) -> str:
        return str(self.value)
