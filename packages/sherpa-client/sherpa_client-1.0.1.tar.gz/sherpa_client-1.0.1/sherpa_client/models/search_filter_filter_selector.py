from enum import Enum


class SearchFilterFilterSelector(str, Enum):
    MUST = "must"
    MUST_NOT = "must_not"

    def __str__(self) -> str:
        return str(self.value)
