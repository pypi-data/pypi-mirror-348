from enum import Enum


class ProjectOpenSessionState(str, Enum):
    CLOSED = "CLOSED"
    NEW = "NEW"
    NOT_EXISTS = "NOT_EXISTS"
    OPEN = "OPEN"
    PAUSED = "PAUSED"
    SAME = "SAME"
    STARTED = "STARTED"
    STOPPED = "STOPPED"

    def __str__(self) -> str:
        return str(self.value)
