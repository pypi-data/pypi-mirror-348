from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SwitchInfoResponseReadonlySwitchesItem")


@_attrs_define
class SwitchInfoResponseReadonlySwitchesItem:
    """
    Attributes:
        id (int):
        name (str):
        description (str):
        value (int):
    """

    id: int
    name: str
    description: str
    value: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Id": id,
                "Name": name,
                "Description": description,
                "Value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("Id")

        name = d.pop("Name")

        description = d.pop("Description")

        value = d.pop("Value")

        switch_info_response_readonly_switches_item = cls(
            id=id,
            name=name,
            description=description,
            value=value,
        )

        switch_info_response_readonly_switches_item.additional_properties = d
        return switch_info_response_readonly_switches_item

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
