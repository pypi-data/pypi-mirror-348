from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_equipment_dome_set_park_position_response_400_error import (
    GetEquipmentDomeSetParkPositionResponse400Error,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetEquipmentDomeSetParkPositionResponse400")


@_attrs_define
class GetEquipmentDomeSetParkPositionResponse400:
    """
    Attributes:
        response (Union[Unset, str]):
        error (Union[Unset, GetEquipmentDomeSetParkPositionResponse400Error]):
        status_code (Union[Unset, int]):  Example: 400.
        success (Union[Unset, bool]):
        type_ (Union[Unset, str]):  Example: API.
    """

    response: Union[Unset, str] = UNSET
    error: Union[Unset, GetEquipmentDomeSetParkPositionResponse400Error] = UNSET
    status_code: Union[Unset, int] = UNSET
    success: Union[Unset, bool] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response

        error: Union[Unset, str] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.value

        status_code = self.status_code

        success = self.success

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if response is not UNSET:
            field_dict["Response"] = response
        if error is not UNSET:
            field_dict["Error"] = error
        if status_code is not UNSET:
            field_dict["StatusCode"] = status_code
        if success is not UNSET:
            field_dict["Success"] = success
        if type_ is not UNSET:
            field_dict["Type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        response = d.pop("Response", UNSET)

        _error = d.pop("Error", UNSET)
        error: Union[Unset, GetEquipmentDomeSetParkPositionResponse400Error]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = GetEquipmentDomeSetParkPositionResponse400Error(_error)

        status_code = d.pop("StatusCode", UNSET)

        success = d.pop("Success", UNSET)

        type_ = d.pop("Type", UNSET)

        get_equipment_dome_set_park_position_response_400 = cls(
            response=response,
            error=error,
            status_code=status_code,
            success=success,
            type_=type_,
        )

        get_equipment_dome_set_park_position_response_400.additional_properties = d
        return get_equipment_dome_set_park_position_response_400

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
