from enum import Enum


class GetSequenceResetResponse409Error(str, Enum):
    NO_DSO_CONTAINER_FOUND = "No DSO Container found"
    SEQUENCE_IS_NOT_INITIALIZED = "Sequence is not initialized"

    def __str__(self) -> str:
        return str(self.value)
