from enum import Enum


class GetImageIndexResponse400Error(str, Enum):
    INDEX_OUT_OF_RANGE = "Index out of range"
    INVALID_BAYER_PATTERN = "Invalid bayer pattern"

    def __str__(self) -> str:
        return str(self.value)
