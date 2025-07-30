from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fw_info_response import FWInfoResponse


T = TypeVar("T", bound="FWInfo")


@_attrs_define
class FWInfo:
    """
    Attributes:
        response (FWInfoResponse):
        error (str):
        status_code (int):
        success (bool):
        type_ (str):
    """

    response: "FWInfoResponse"
    error: str
    status_code: int
    success: bool
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response.to_dict()

        error = self.error

        status_code = self.status_code

        success = self.success

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Response": response,
                "Error": error,
                "StatusCode": status_code,
                "Success": success,
                "Type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fw_info_response import FWInfoResponse

        d = dict(src_dict)
        response = FWInfoResponse.from_dict(d.pop("Response"))

        error = d.pop("Error")

        status_code = d.pop("StatusCode")

        success = d.pop("Success")

        type_ = d.pop("Type")

        fw_info = cls(
            response=response,
            error=error,
            status_code=status_code,
            success=success,
            type_=type_,
        )

        fw_info.additional_properties = d
        return fw_info

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
