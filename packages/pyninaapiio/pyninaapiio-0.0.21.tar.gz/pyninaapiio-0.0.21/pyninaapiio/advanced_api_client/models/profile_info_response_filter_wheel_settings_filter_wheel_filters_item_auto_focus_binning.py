from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileInfoResponseFilterWheelSettingsFilterWheelFiltersItemAutoFocusBinning")


@_attrs_define
class ProfileInfoResponseFilterWheelSettingsFilterWheelFiltersItemAutoFocusBinning:
    """
    Attributes:
        name (Union[Unset, str]):
        x (Union[Unset, int]):
        y (Union[Unset, int]):
    """

    name: Union[Unset, str] = UNSET
    x: Union[Unset, int] = UNSET
    y: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        x = self.x

        y = self.y

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["Name"] = name
        if x is not UNSET:
            field_dict["X"] = x
        if y is not UNSET:
            field_dict["Y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("Name", UNSET)

        x = d.pop("X", UNSET)

        y = d.pop("Y", UNSET)

        profile_info_response_filter_wheel_settings_filter_wheel_filters_item_auto_focus_binning = cls(
            name=name,
            x=x,
            y=y,
        )

        profile_info_response_filter_wheel_settings_filter_wheel_filters_item_auto_focus_binning.additional_properties = d
        return profile_info_response_filter_wheel_settings_filter_wheel_filters_item_auto_focus_binning

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
