from enum import Enum


class GetEquipmentMountSlewStopResponse409Error(str, Enum):
    MOUNT_NOT_CONNECTED = "Mount not connected"
    MOUNT_NOT_SLEWING = "Mount not slewing"

    def __str__(self) -> str:
        return str(self.value)
