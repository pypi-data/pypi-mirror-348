from enum import Enum


class QuestionAnsweringParamsLanguageDetection(str, Enum):
    FIRST_HIT = "first_hit"
    PROJECT = "project"
    INTERFACE = "interface"
    BROWSER = "browser"
    SPECIFIC = "specific"

    def __str__(self) -> str:
        return str(self.value)
