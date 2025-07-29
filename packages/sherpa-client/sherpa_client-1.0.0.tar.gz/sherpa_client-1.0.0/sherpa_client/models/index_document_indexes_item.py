from enum import Enum


class IndexDocumentIndexesItem(str, Enum):
    DOCUMENT = "document"
    SEGMENT = "segment"
    TERM = "term"

    def __str__(self) -> str:
        return str(self.value)
