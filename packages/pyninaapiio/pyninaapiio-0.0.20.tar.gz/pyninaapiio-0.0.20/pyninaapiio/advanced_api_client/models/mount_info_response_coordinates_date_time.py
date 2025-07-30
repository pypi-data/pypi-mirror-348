from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MountInfoResponseCoordinatesDateTime")


@_attrs_define
class MountInfoResponseCoordinatesDateTime:
    """
    Attributes:
        now (str):
        utc_now (str):
    """

    now: str
    utc_now: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        now = self.now

        utc_now = self.utc_now

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Now": now,
                "UtcNow": utc_now,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        now = d.pop("Now")

        utc_now = d.pop("UtcNow")

        mount_info_response_coordinates_date_time = cls(
            now=now,
            utc_now=utc_now,
        )

        mount_info_response_coordinates_date_time.additional_properties = d
        return mount_info_response_coordinates_date_time

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
