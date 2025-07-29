from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.guider_info_response_rms_error_dec import GuiderInfoResponseRMSErrorDec
    from ..models.guider_info_response_rms_error_peak_dec import GuiderInfoResponseRMSErrorPeakDec
    from ..models.guider_info_response_rms_error_peak_ra import GuiderInfoResponseRMSErrorPeakRA
    from ..models.guider_info_response_rms_error_ra import GuiderInfoResponseRMSErrorRA
    from ..models.guider_info_response_rms_error_total import GuiderInfoResponseRMSErrorTotal


T = TypeVar("T", bound="GuiderInfoResponseRMSError")


@_attrs_define
class GuiderInfoResponseRMSError:
    """
    Attributes:
        ra (GuiderInfoResponseRMSErrorRA):
        dec (GuiderInfoResponseRMSErrorDec):
        total (GuiderInfoResponseRMSErrorTotal):
        peak_ra (GuiderInfoResponseRMSErrorPeakRA):
        peak_dec (GuiderInfoResponseRMSErrorPeakDec):
    """

    ra: "GuiderInfoResponseRMSErrorRA"
    dec: "GuiderInfoResponseRMSErrorDec"
    total: "GuiderInfoResponseRMSErrorTotal"
    peak_ra: "GuiderInfoResponseRMSErrorPeakRA"
    peak_dec: "GuiderInfoResponseRMSErrorPeakDec"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ra = self.ra.to_dict()

        dec = self.dec.to_dict()

        total = self.total.to_dict()

        peak_ra = self.peak_ra.to_dict()

        peak_dec = self.peak_dec.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "RA": ra,
                "Dec": dec,
                "Total": total,
                "PeakRA": peak_ra,
                "PeakDec": peak_dec,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guider_info_response_rms_error_dec import GuiderInfoResponseRMSErrorDec
        from ..models.guider_info_response_rms_error_peak_dec import GuiderInfoResponseRMSErrorPeakDec
        from ..models.guider_info_response_rms_error_peak_ra import GuiderInfoResponseRMSErrorPeakRA
        from ..models.guider_info_response_rms_error_ra import GuiderInfoResponseRMSErrorRA
        from ..models.guider_info_response_rms_error_total import GuiderInfoResponseRMSErrorTotal

        d = dict(src_dict)
        ra = GuiderInfoResponseRMSErrorRA.from_dict(d.pop("RA"))

        dec = GuiderInfoResponseRMSErrorDec.from_dict(d.pop("Dec"))

        total = GuiderInfoResponseRMSErrorTotal.from_dict(d.pop("Total"))

        peak_ra = GuiderInfoResponseRMSErrorPeakRA.from_dict(d.pop("PeakRA"))

        peak_dec = GuiderInfoResponseRMSErrorPeakDec.from_dict(d.pop("PeakDec"))

        guider_info_response_rms_error = cls(
            ra=ra,
            dec=dec,
            total=total,
            peak_ra=peak_ra,
            peak_dec=peak_dec,
        )

        guider_info_response_rms_error.additional_properties = d
        return guider_info_response_rms_error

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
