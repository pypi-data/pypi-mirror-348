from enum import Enum


class SherpaJobBeanStatus(str, Enum):
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    STARTED = "STARTED"

    def __str__(self) -> str:
        return str(self.value)
