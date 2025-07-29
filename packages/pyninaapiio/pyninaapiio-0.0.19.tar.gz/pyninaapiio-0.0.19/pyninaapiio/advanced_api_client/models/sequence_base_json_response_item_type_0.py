from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SequenceBaseJsonResponseItemType0")


@_attrs_define
class SequenceBaseJsonResponseItemType0:
    """
    Attributes:
        conditions (Union[Unset, list[Any]]):
        items (Union[Unset, list[Any]]): Contains sequence instructions as well as containers
        triggers (Union[Unset, list[Any]]):
        status (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    conditions: Union[Unset, list[Any]] = UNSET
    items: Union[Unset, list[Any]] = UNSET
    triggers: Union[Unset, list[Any]] = UNSET
    status: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conditions: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = self.conditions

        items: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items

        triggers: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = self.triggers

        status = self.status

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conditions is not UNSET:
            field_dict["Conditions"] = conditions
        if items is not UNSET:
            field_dict["Items"] = items
        if triggers is not UNSET:
            field_dict["Triggers"] = triggers
        if status is not UNSET:
            field_dict["Status"] = status
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        conditions = cast(list[Any], d.pop("Conditions", UNSET))

        items = cast(list[Any], d.pop("Items", UNSET))

        triggers = cast(list[Any], d.pop("Triggers", UNSET))

        status = d.pop("Status", UNSET)

        name = d.pop("Name", UNSET)

        sequence_base_json_response_item_type_0 = cls(
            conditions=conditions,
            items=items,
            triggers=triggers,
            status=status,
            name=name,
        )

        sequence_base_json_response_item_type_0.additional_properties = d
        return sequence_base_json_response_item_type_0

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
