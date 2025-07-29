from enum import Enum


class QuestionAnsweringParamsLanguageDetection(str, Enum):
    BROWSER = "browser"
    FIRST_HIT = "first_hit"
    INTERFACE = "interface"
    PROJECT = "project"
    SPECIFIC = "specific"

    def __str__(self) -> str:
        return str(self.value)
