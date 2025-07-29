from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FocuserLastAFResponsePreviousFocusPoint")


@_attrs_define
class FocuserLastAFResponsePreviousFocusPoint:
    """
    Attributes:
        position (float):
        value (float):
        error (int):
    """

    position: float
    value: float
    error: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        position = self.position

        value = self.value

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Position": position,
                "Value": value,
                "Error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        position = d.pop("Position")

        value = d.pop("Value")

        error = d.pop("Error")

        focuser_last_af_response_previous_focus_point = cls(
            position=position,
            value=value,
            error=error,
        )

        focuser_last_af_response_previous_focus_point.additional_properties = d
        return focuser_last_af_response_previous_focus_point

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
