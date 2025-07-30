from enum import Enum


class GetSequenceJsonResponse409Error(str, Enum):
    NO_DSO_CONTAINER_FOUND = "No DSO container found"
    SEQUENCER_NOT_INITIALIZED = "Sequencer not initialized"

    def __str__(self) -> str:
        return str(self.value)
