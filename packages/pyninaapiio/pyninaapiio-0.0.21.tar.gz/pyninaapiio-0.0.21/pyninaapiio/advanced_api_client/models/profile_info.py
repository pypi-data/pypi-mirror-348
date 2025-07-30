from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_info_response import ProfileInfoResponse


T = TypeVar("T", bound="ProfileInfo")


@_attrs_define
class ProfileInfo:
    """
    Attributes:
        response (Union[Unset, ProfileInfoResponse]):
        error (Union[Unset, str]):
        status_code (Union[Unset, int]):  Example: 200.
        success (Union[Unset, bool]):  Example: True.
        type_ (Union[Unset, str]):  Example: API.
    """

    response: Union[Unset, "ProfileInfoResponse"] = UNSET
    error: Union[Unset, str] = UNSET
    status_code: Union[Unset, int] = UNSET
    success: Union[Unset, bool] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict()

        error = self.error

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
        from ..models.profile_info_response import ProfileInfoResponse

        d = dict(src_dict)
        _response = d.pop("Response", UNSET)
        response: Union[Unset, ProfileInfoResponse]
        if isinstance(_response, Unset):
            response = UNSET
        else:
            response = ProfileInfoResponse.from_dict(_response)

        error = d.pop("Error", UNSET)

        status_code = d.pop("StatusCode", UNSET)

        success = d.pop("Success", UNSET)

        type_ = d.pop("Type", UNSET)

        profile_info = cls(
            response=response,
            error=error,
            status_code=status_code,
            success=success,
            type_=type_,
        )

        profile_info.additional_properties = d
        return profile_info

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
