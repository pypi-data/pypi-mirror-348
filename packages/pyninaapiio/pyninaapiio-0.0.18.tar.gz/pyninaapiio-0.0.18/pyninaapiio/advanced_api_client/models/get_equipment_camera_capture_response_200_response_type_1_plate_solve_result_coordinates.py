from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetEquipmentCameraCaptureResponse200ResponseType1PlateSolveResultCoordinates")


@_attrs_define
class GetEquipmentCameraCaptureResponse200ResponseType1PlateSolveResultCoordinates:
    """
    Attributes:
        ra (Union[Unset, float]):
        ra_degrees (Union[Unset, float]):
        dec (Union[Unset, float]):
        dec_degrees (Union[Unset, float]):
        epoch (Union[Unset, int]):
    """

    ra: Union[Unset, float] = UNSET
    ra_degrees: Union[Unset, float] = UNSET
    dec: Union[Unset, float] = UNSET
    dec_degrees: Union[Unset, float] = UNSET
    epoch: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ra = self.ra

        ra_degrees = self.ra_degrees

        dec = self.dec

        dec_degrees = self.dec_degrees

        epoch = self.epoch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ra is not UNSET:
            field_dict["RA"] = ra
        if ra_degrees is not UNSET:
            field_dict["RADegrees"] = ra_degrees
        if dec is not UNSET:
            field_dict["Dec"] = dec
        if dec_degrees is not UNSET:
            field_dict["DECDegrees"] = dec_degrees
        if epoch is not UNSET:
            field_dict["Epoch"] = epoch

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ra = d.pop("RA", UNSET)

        ra_degrees = d.pop("RADegrees", UNSET)

        dec = d.pop("Dec", UNSET)

        dec_degrees = d.pop("DECDegrees", UNSET)

        epoch = d.pop("Epoch", UNSET)

        get_equipment_camera_capture_response_200_response_type_1_plate_solve_result_coordinates = cls(
            ra=ra,
            ra_degrees=ra_degrees,
            dec=dec,
            dec_degrees=dec_degrees,
            epoch=epoch,
        )

        get_equipment_camera_capture_response_200_response_type_1_plate_solve_result_coordinates.additional_properties = d
        return get_equipment_camera_capture_response_200_response_type_1_plate_solve_result_coordinates

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
