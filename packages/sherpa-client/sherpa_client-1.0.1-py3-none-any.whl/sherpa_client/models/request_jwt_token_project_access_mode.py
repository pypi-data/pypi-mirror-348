from enum import Enum


class RequestJwtTokenProjectAccessMode(str, Enum):
    CHMOD = "chmod"
    READ = "read"
    WRITE = "write"

    def __str__(self) -> str:
        return str(self.value)
