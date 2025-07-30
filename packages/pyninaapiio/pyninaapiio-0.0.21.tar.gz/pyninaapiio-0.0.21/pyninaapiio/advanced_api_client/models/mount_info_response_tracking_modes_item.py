from enum import Enum


class MountInfoResponseTrackingModesItem(str, Enum):
    CUSTOM = "Custom"
    KING = "King"
    LUNAR = "Lunar"
    SIDERIAL = "Siderial"
    SIDEREAL = "Sidereal"
    SOLAR = "Solar"
    STOPPED = "Stopped"

    def __str__(self) -> str:
        return str(self.value)
