"""Defines the Data Classes used."""

# import math
# from dataclasses import dataclass
# from datetime import datetime
# from pprint import pprint as pp
from datetime import datetime
from typing import Any, Optional, TypedDict

from typeguard import typechecked

from .advanced_api_client.models.dome_info_response_shutter_status import DomeInfoResponseShutterStatus
from .advanced_api_client.models.fw_info_response_available_filters_item import (
    FWInfoResponseAvailableFiltersItem,
)
from .advanced_api_client.models.fw_info_response_selected_filter import FWInfoResponseSelectedFilter
from .advanced_api_client.models.guider_info_response_last_guide_step import GuiderInfoResponseLastGuideStep
from .advanced_api_client.models.guider_info_response_rms_error import GuiderInfoResponseRMSError
from .advanced_api_client.models.guider_info_response_state import GuiderInfoResponseState
from .advanced_api_client.models.mount_info_response_alignment_mode import MountInfoResponseAlignmentMode
from .advanced_api_client.models.mount_info_response_coordinates import MountInfoResponseCoordinates
from .advanced_api_client.models.mount_info_response_equatorial_system import (
    MountInfoResponseEquatorialSystem,
)
from .advanced_api_client.models.mount_info_response_primary_axis_rates_item import (
    MountInfoResponsePrimaryAxisRatesItem,
)
from .advanced_api_client.models.mount_info_response_secondary_axis_rates_item import (
    MountInfoResponseSecondaryAxisRatesItem,
)
from .advanced_api_client.models.mount_info_response_side_of_pier import MountInfoResponseSideOfPier
from .advanced_api_client.models.mount_info_response_tracking_modes_item import (
    MountInfoResponseTrackingModesItem,
)
from .advanced_api_client.models.mount_info_response_tracking_rate import MountInfoResponseTrackingRate
from .advanced_api_client.types import Unset


# #########################################################################
# Application
# #########################################################################
class ApplicationDataModel(TypedDict, total=False):
    Connected: bool
    Version: str


@typechecked
class ApplicationData:
    def __init__(self, *, data: ApplicationDataModel):
        self.version = data.get("Version")
        self.connected = data.get("Connected")
        # self.screenshot


# #########################################################################
# Camera
# #########################################################################
class CameraDataModel(TypedDict, total=False):
    Connected: bool
    Name: str
    DisplayName: str
    AtTargetTemp: bool
    Battery: int
    BayerOffsetX: int
    BayerOffsetY: int
    BinningModes: list[Any]
    BinX: int
    BinY: int
    BitDepth: int
    CameraState: str
    CanGetGain: bool
    CanSetGain: bool
    CanSetOffset: bool
    CanSetTemperature: bool
    CanSetUSBLimit: bool
    CanShowLiveView: bool
    CanSubSample: bool
    CoolerOn: bool
    CoolerPower: int
    DefaultGain: int
    DefaultOffset: int
    DeviceId: str
    DewHeaterOn: bool
    ElectronsPerADU: int | Any
    ExposureEndTime: str
    ExposureMax: int | Any
    ExposureMin: int | Any
    Gain: int
    GainMax: int
    GainMin: int
    Gains: list[Any]
    HasDewHeater: bool
    HasShutter: bool
    IsExposing: bool
    IsSubSampleEnabled: bool
    LastDownloadTime: int
    LiveViewEnabled: bool
    Offset: int
    OffsetMax: int
    OffsetMin: int
    PixelSize: int | Any
    ReadoutMode: int | str
    ReadoutModeForNormalImages: int | str
    ReadoutModeForSnapImages: int | str
    ReadoutModes: list[str]
    SensorType: str
    SubSampleHeight: int
    SubSampleWidth: int
    SubSampleX: int
    SubSampleY: int
    SupportedActions: list[str]
    TargetTemp: float
    Temperature: int
    TemperatureSetPoint: int
    USBLimit: int
    USBLimitMax: int
    USBLimitMin: int
    XSize: int
    YSize: int


@typechecked
class CameraData:
    def __init__(self, *, data: CameraDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.at_target_temp = data.get("AtTargetTemp")
        self.battery = data.get("Battery")
        self.bayer_offset_x = data.get("BayerOffsetX")
        self.bayer_offset_y = data.get("BayerOffsetY")
        self.bin_x = data.get("BinX")
        self.bin_y = data.get("BinY")
        self.binning_modes = data.get("BinningModes")
        self.bit_depth = data.get("BitDepth")
        self.camera_state = data.get("CameraState")
        self.can_get_gain = data.get("CanGetGain")
        self.can_set_gain = data.get("CanSetGain")
        self.can_set_offset = data.get("CanSetOffset")
        self.can_set_temperature = data.get("CanSetTemperature")
        self.can_set_usb_limit = data.get("CanSetUSBLimit")
        self.can_show_live_view = data.get("CanShowLiveView")
        self.can_sub_sample = data.get("CanSubSample")
        self.cooler_on = data.get("CoolerOn")
        self.cooler_power = data.get("CoolerPower")
        self.default_gain = data.get("DefaultGain")
        self.default_offset = data.get("DefaultOffset")
        self.device_id = data.get("DeviceId")
        self.dew_heater_on = data.get("DewHeaterOn")
        self.electrons_per_adu = data.get("ElectronsPerADU")
        self.exposure_end_time = data.get("ExposureEndTime")
        self.exposure_max = data.get("ExposureMax")
        self.exposure_min = data.get("ExposureMin")
        self.gain = data.get("Gain")
        self.gain_max = data.get("GainMax")
        self.gain_min = data.get("GainMin")
        self.gains = data.get("Gains")
        self.has_dew_heater = data.get("HasDewHeater")
        self.has_shutter = data.get("HasShutter")
        self.is_exposing = data.get("IsExposing")
        self.is_sub_sample_enabled = data.get("IsSubSampleEnabled")
        self.last_download_time = data.get("LastDownloadTime")
        self.live_view_enabled = data.get("LiveViewEnabled")
        self.offset = data.get("Offset")
        self.offset_max = data.get("OffsetMax")
        self.offset_min = data.get("OffsetMin")
        self.pixel_size = data.get("PixelSize")
        self.readout_mode = (
            data.get("ReadoutModes")[data.get("ReadoutMode")]
            if data.get("ReadoutMode") is not None and data.get("ReadoutModes") is not None
            else None
        )
        self.readout_mode_for_normal_images = (
            data.get("ReadoutModes")[data.get("ReadoutModeForNormalImages")]
            if data.get("ReadoutModeForNormalImages") is not None and data.get("ReadoutModes") is not None
            else None
        )
        self.readout_mode_for_snap_images = (
            data.get("ReadoutModes")[data.get("ReadoutModeForSnapImages")]
            if data.get("ReadoutModeForSnapImages") is not None and data.get("ReadoutModes") is not None
            else None
        )
        self.readout_modes = data.get("ReadoutModes")
        self.sensor_type = data.get("SensorType")
        self.sub_sample_height = data.get("SubSampleHeight")
        self.sub_sample_width = data.get("SubSampleWidth")
        self.sub_sample_x = data.get("SubSampleX")
        self.sub_sample_y = data.get("SubSampleY")
        self.supported_actions = data.get("SupportedActions")
        self.target_temp = data.get("TargetTemp")
        self.temperature = data.get("Temperature")
        self.temperature_set_point = data.get("TemperatureSetPoint")
        self.usb_limit = data.get("USBLimit")
        self.usb_limit_max = data.get("USBLimitMax")
        self.usb_limit_min = data.get("USBLimitMin")
        self.x_size = data.get("XSize")
        self.y_size = data.get("YSize")


# #########################################################################
# Dome
# #########################################################################
class DomeDataModel(TypedDict, total=False):
    Connected: bool
    Name: str | Unset
    DisplayName: str | Unset
    Description: str
    Altitude: float | str
    AltitudeDMS: str
    ApplicationFollowing: bool
    AtHome: bool
    AtPark: bool
    Azimuth: float | str
    AzimuthDMS: str
    CanFindHome: bool
    CanPark: bool
    CanSetAzimuth: bool
    CanSetPark: bool
    CanSetShutter: bool
    CanSyncAzimuth: bool
    DeviceId: str
    DriverCanFollow: bool
    DriverFollowing: bool
    DriverInfo: str
    DriverVersion: str
    FollowingType: str
    IsFollowing: bool
    IsSynchronized: bool
    ShutterStatus: str  # DomeInfoResponseShutterStatus
    Slewing: bool
    SupportedActions: list[Any]


@typechecked
class DomeData:
    def __init__(self, *, data: DomeDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.altitude = data.get("Altitude")
        self.altitude_dms = data.get("AltitudeDMS")
        self.application_following = data.get("ApplicationFollowing")
        self.at_home = data.get("AtHome")
        self.at_park = data.get("AtPark")
        self.azimuth = data.get("Azimuth")
        self.azimuth_dms = data.get("AzimuthDMS")
        self.can_find_home = data.get("CanFindHome")
        self.can_park = data.get("CanPark")
        self.can_set_azimuth = data.get("CanSetAzimuth")
        self.can_set_park = data.get("CanSetPark")
        self.can_set_shutter = data.get("CanSetShutter")
        self.can_sync_azimuth = data.get("CanSyncAzimuth")
        self.device_id = data.get("DeviceId")
        self.driver_can_follow = data.get("DriverCanFollow")
        self.driver_following = data.get("DriverFollowing")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.following_type = data.get("FollowingType")
        self.is_following = data.get("IsFollowing")
        self.is_synchronized = data.get("IsSynchronized")
        self.shutter_status = data.get("ShutterStatus")
        self.slewing = data.get("Slewing")
        self.supported_actions = data.get("SupportedActions")


# #########################################################################
# FilterWheel
# #########################################################################
class FilterWheelDataModel(TypedDict, total=False):
    Connected: bool
    Name: str | Unset
    DisplayName: str | Unset
    AvailableFilters: list[Any]
    Description: str
    DeviceId: str
    DriverInfo: str
    DriverVersion: str
    IsMoving: bool
    SelectedFilter: Any  # FWInfoResponseSelectedFilter
    SupportedActions: list[Any]


@typechecked
class FilterWheelData:
    def __init__(self, *, data: FilterWheelDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.available_filters = data.get("AvailableFilters")
        self.description = data.get("Description")
        self.device_id = data.get("DeviceId")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.is_moving = data.get("IsMoving")
        self.selected_filter = data.get("SelectedFilter")
        self.supported_actions = data.get("SupportedActions")

    @property
    def selected_filter_id(self) -> int:
        return self.selected_filter.get("Id") if self.selected_filter is not None else -1

    @property
    def selected_filter_name(self) -> str:
        return self.selected_filter.get("Name") if self.selected_filter is not None else ""


# #########################################################################
# Focuser
# #########################################################################
class FocuserDataModel(TypedDict, total=False):
    Connected: bool
    Name: str | Unset
    DisplayName: str | Unset
    Description: str
    DeviceId: str
    DriverInfo: str
    DriverVersion: str
    IsMoving: bool
    IsSettling: bool
    Position: int
    StepSize: int
    SupportedActions: list[Any]
    TempComp: bool
    TempCompAvailable: bool
    Temperature: float


@typechecked
class FocuserData:
    def __init__(self, *, data: FocuserDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.device_id = data.get("DeviceId")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.is_moving = data.get("IsMoving")
        self.is_settling = data.get("IsSettling")
        self.position = data.get("Position")
        self.step_size = data.get("StepSize")
        self.supported_actions = data.get("SupportedActions")
        self.temp_comp = data.get("TempComp")
        self.temp_comp_available = data.get("TempCompAvailable")
        self.temperature = data.get("Temperature")


# #########################################################################
# Guider
# #########################################################################
class GuiderDataModel(TypedDict, total=False):
    Connected: bool
    Name: str | Unset
    DisplayName: str
    CanClearCalibration: bool
    CanGetLockPosition: bool
    CanSetShiftRate: bool
    Description: str
    DeviceId: str
    DriverInfo: str
    DriverVersion: str
    LastGuideStep: Optional[GuiderInfoResponseLastGuideStep]
    PixelScale: float
    RMSError: Any  # GuiderInfoResponseRMSError
    State: Any  # GuiderInfoResponseState
    SupportedActions: list[Any]


@typechecked
class GuiderData:
    def __init__(self, *, data: GuiderDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.can_clear_calibration = data.get("CanClearCalibration")
        self.can_get_lock_position = data.get("CanGetLockPosition")
        self.can_set_shift_rate = data.get("CanSetShiftRate")
        self.description = data.get("Description")
        self.device_id = data.get("DeviceId")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.last_guide_step = data.get("LastGuideStep")
        self.pixel_scale = data.get("PixelScale")
        self.rms_error = data.get("RMSError")
        self.state = data.get("State")
        self.supported_actions = data.get("SupportedActions")

    @property
    def last_guide_step_ra(self) -> float:
        return self.last_guide_step.get("RADistanceRaw") if self.last_guide_step is not None else 0

    @property
    def last_guide_step_dec(self) -> float:
        return self.last_guide_step.get("DECDistanceRaw") if self.last_guide_step is not None else 0

    @property
    def rms_error_ra_arcsec(self) -> float:
        return self.rms_error.get("RA").get("Arcseconds") if self.rms_error is not None else 0

    @property
    def rms_error_ra_peak_arcsec(self) -> float:
        return self.rms_error.get("PeakRA").get("Arcseconds") if self.rms_error is not None else 0

    @property
    def rms_error_dec_arcsec(self) -> float:
        return self.rms_error.get("Dec").get("Arcseconds") if self.rms_error is not None else 0

    @property
    def rms_error_dec_peak_arcsec(self) -> float:
        return self.rms_error.get("PeakDec").get("Arcseconds") if self.rms_error is not None else 0

    @property
    def rms_error_total_arcsec(self) -> float:
        return self.rms_error.get("Total").get("Arcseconds") if self.rms_error is not None else 0


# #########################################################################
# Image
# #########################################################################
class ImageDataModel(TypedDict, total=False):
    Connected: bool
    CameraName: str
    Date: datetime
    DecodedData: bytes
    DecodedDataLength: int
    ExposureTime: int
    Filter: str
    FocalLength: int
    Gain: int
    HFR: float
    ImageType: str  # GetImageHistoryResponse200ResponseType0ItemImageType
    IndexLatest: int
    IsBayered: bool
    Mean: int
    Median: int
    Offset: int
    RmsText: str
    Stars: int
    StDev: float
    TelescopeName: str
    Temperature: float


@typechecked
class ImageData:
    def __init__(self, *, data: ImageDataModel):
        self.connected = data.get("Connected")
        self.camera_name = data.get("CameraName")
        self.date = data.get("Date")
        self.decoded_data = data.get("DecodedData")
        self.decoded_data_length = data.get("DecodedDataLength")
        self.exposure_time = data.get("ExposureTime")
        self.filter = data.get("Filter")
        self.focal_length = data.get("FocalLength")
        self.gain = data.get("Gain")
        self.hfr = round(data.get("HFR"), 3) if data.get("HFR") is not None else None
        self.image_type = data.get("ImageType")
        self.index_latest = data.get("IndexLatest")
        self.is_bayered = data.get("IsBayered")
        self.mean = int(data.get("Mean")) if data.get("Mean") is not None else None
        self.median = int(data.get("Median")) if data.get("Median") is not None else None
        self.offset = data.get("Offset")
        self.rms_text = data.get("RmsText")
        self.st_dev = round(data.get("StDev"), 3) if data.get("StDev") is not None else None
        self.stars = data.get("Stars")
        self.telescope_name = data.get("TelescopeName")
        self.temperature = data.get("Temperature")


# #########################################################################
# Mount
# #########################################################################
# class DeviceMountListDataModel(TypedDict):
#     items: dict


# @typechecked
# class DeviceMountListData:
#     """A representation of the geographic location."""

#     def __init__(self, *, data: DeviceMountListDataModel):
#         self.items = data.get("items")


# class DeviceMountDataModel(TypedDict):
#     HasSetupDialog: bool | Unset
#     Id: str | Unset
#     Name: str | Unset
#     DisplayName: str | Unset
#     Category: str | Unset
#     Connected: bool
#     Description: str | Unset
#     DriverInfo: str | Unset
#     DriverVersion: str | Unset
#     SupportedActions: list | Unset
#     # additional_properties: dict


# @typechecked
# class DeviceMountData:
#     """A representation of the geographic location."""

#     def __init__(self, *, data: DeviceMountDataModel):
#         print("init")
#         self.has_setup_dialog = data.get("HasSetupDialog")
#         self.id = data.get("Id")
#         self.name = data.get("Name")
#         self.display_name = data.get("DisplayName")
#         self.category = data.get("Category")
#         self.connected = data.get("Connected")
#         self.description = data.get("Description")
#         self.driver_info = data.get("DriverInfo")
#         self.driver_version = data.get("DriverVersion")
#         self.supported_actions = data.get("SupportedActions")
#         # self.additional_properties = data.get("additional_properties")


class MountDataModel(TypedDict, total=False):
    Connected: bool
    Name: str | Unset
    DisplayName: str | Unset
    AlignmentMode: MountInfoResponseAlignmentMode | Any
    Altitude: float | str
    AltitudeString: str
    AtHome: bool
    AtPark: bool
    Azimuth: float | str
    AzimuthString: str
    CanFindHome: bool
    CanMovePrimaryAxis: bool
    CanMoveSecondaryAxis: bool
    CanPark: bool
    CanPulseGuide: bool
    CanSetDeclinationRate: bool
    CanSetPark: bool
    CanSetPierSide: bool
    CanSetRightAscensionRate: bool
    CanSetTrackingEnabled: bool
    CanSlew: bool
    Coordinates: MountInfoResponseCoordinates | Any
    Declination: float
    DeclinationString: str
    DeviceId: str | Unset
    EquatorialSystem: MountInfoResponseEquatorialSystem | Any
    GuideRateDeclinationArcsecPerSec: int | Any
    GuideRateRightAscensionArcsecPerSec: int | Any
    HasUnknownEpoch: bool
    HoursToMeridianString: str
    IsPulseGuiding: bool
    PrimaryAxisRates: MountInfoResponsePrimaryAxisRatesItem | Any
    RightAscension: float
    RightAscensionString: str
    SecondaryAxisRates: MountInfoResponseSecondaryAxisRatesItem | Any
    SideOfPier: MountInfoResponseSideOfPier | Any
    SiderealTime: float
    SiderealTimeString: str
    SiteElevation: float
    SiteLatitude: float
    SiteLongitude: float
    Slewing: bool
    SupportedActions: list[str]
    TargetCoordinates: Any
    TimeToMeridianFlip: float
    TimeToMeridianFlipString: str
    TrackingEnabled: bool
    TrackingModes: MountInfoResponseTrackingModesItem | Any
    TrackingRate: MountInfoResponseTrackingRate | Any
    UTCDate: str


@typechecked
class MountData:
    """A representation of the geographic location."""

    def __init__(self, *, data: MountDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.alignment_mode = data.get("AlignmentMode")
        self.altitude = (
            round(data.get("Altitude"), 3)
            if data.get("Altitude") is not None and data.get("Altitude") != "NaN"
            else None
        )
        self.altitude_string = data.get("AltitudeString")
        self.at_home = data.get("AtHome")
        self.at_park = data.get("AtPark")
        self.azimuth = (
            round(data.get("Azimuth"), 3) if data.get("Azimuth") is not None and data.get("Azimuth") != "NaN" else None
        )
        self.azimuth_string = data.get("AzimuthString")
        self.can_find_home = data.get("CanFindHome")
        self.can_move_primary_axis = data.get("CanMovePrimaryAxis")
        self.can_move_secondary_axis = data.get("CanMoveSecondaryAxis")
        self.can_park = data.get("CanPark")
        self.can_pulse_guide = data.get("CanPulseGuide")
        self.can_set_declination_rate = data.get("CanSetDeclinationRate")
        self.can_set_park = data.get("CanSetPark")
        self.can_set_pier_side = data.get("CanSetPierSide")
        self.can_set_right_ascension_rate = data.get("CanSetRightAscensionRate")
        self.can_set_tracking_enabled = data.get("CanSetTrackingEnabled")
        self.can_slew = data.get("CanSlew")
        self.coordinates = data.get("Coordinates")
        self.declination = data.get("Declination")
        self.declination_string = data.get("DeclinationString")
        self.device_id = data.get("DeviceId")
        self.equatorial_system = data.get("EquatorialSystem")
        self.guide_rate_declination_arcsec_per_sec = data.get("GuideRateDeclinationArcsecPerSec")
        self.guide_rate_right_ascension_arcsec_per_sec = data.get("GuideRateRightAscensionArcsecPerSec")
        self.has_unknown_epoch = data.get("HasUnknownEpoch")
        self.hours_to_meridian_string = data.get("HoursToMeridianString")
        self.is_pulse_guiding = data.get("IsPulseGuiding")
        self.primary_axis_rates = data.get("PrimaryAxisRates")
        self.right_ascension = round(data.get("RightAscension"), 3) if data.get("RightAscension") is not None else None
        self.right_ascension_string = data.get("RightAscensionString")
        self.secondary_axis_rates = data.get("SecondaryAxisRates")
        self.side_of_pier = data.get("SideOfPier")
        self.sidereal_time = data.get("SiderealTime")
        self.sidereal_time_string = data.get("SiderealTimeString")
        self.site_elevation = data.get("SiteElevation")
        self.site_latitude = round(data.get("SiteLatitude"), 3) if data.get("SiteLatitude") is not None else None
        self.site_longitude = round(data.get("SiteLongitude"), 3) if data.get("SiteLongitude") is not None else None
        self.slewing = data.get("Slewing")
        self.supported_actions = data.get("SupportedActions")
        self.target_coordinates = data.get("TargetCoordinates")
        self.time_to_meridian_flip = data.get("TimeToMeridianFlip")
        self.time_to_meridian_flip_string = data.get("TimeToMeridianFlipString")
        self.tracking_enabled = data.get("TrackingEnabled")
        self.tracking_modes = data.get("TrackingModes")
        self.tracking_rate = data.get("TrackingRate")
        self.utc_date = data.get("UTCDate")

    @property
    def coordinates_ra(self) -> float:
        return (
            round(self.coordinates.get("RA"), 3)
            if self.coordinates is not None and self.coordinates.get("RA") is not None
            else 0
        )

    @property
    def coordinates_ra_str(self) -> str:
        return (
            self.coordinates.get("RAString")
            if self.coordinates is not None and self.coordinates.get("RAString") is not None
            else ""
        )

    @property
    def coordinates_dec(self) -> float:
        return (
            round(self.coordinates.get("Dec"), 3)
            if self.coordinates is not None and self.coordinates.get("Dec") is not None
            else 0
        )

    @property
    def coordinates_dec_str(self) -> str:
        return (
            self.coordinates.get("DecString")
            if self.coordinates is not None and self.coordinates.get("DecString") is not None
            else ""
        )


# #########################################################################
# Rotator
# #########################################################################
class RotatorDataModel(TypedDict, total=False):
    # device_list_response_item

    Connected: bool
    Name: str
    DisplayName: str
    Description: str

    CanReverse: bool
    Reverse: bool
    MechanicalPosition: int
    Position: int
    StepSize: float
    IsMoving: bool
    Synced: bool
    SupportedActions: list[Any]
    DriverInfo: str
    DriverVersion: str
    DeviceId: str
    AdditionalProperties: dict[str, Any]


@typechecked
class RotatorData:
    """A representation of the geographic location."""

    def __init__(self, *, data: RotatorDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")

        self.can_reverse = data.get("CanReverse")
        self.reverse = data.get("Reverse")
        self.mechanical_position = data.get("MechanicalPosition")
        self.position = data.get("Position")
        self.step_size = data.get("StepSize")
        self.is_moving = data.get("IsMoving")
        self.synced = data.get("Synced")
        self.supported_actions = data.get("SupportedActions")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.device_id = data.get("DeviceId")
        self.additional_properties = data.get("Name")


# #########################################################################
# SafetyMonitor
# #########################################################################
class SafetyMonitorDataModel(TypedDict, total=False):
    # device_list_response_item

    Connected: bool
    Name: str
    DisplayName: str
    Description: str
    DriverInfo: str
    DriverVersion: str
    DeviceId: str

    IsSafe: bool
    SupportedActions: list[Any]


@typechecked
class SafetyMonitorData:
    """A representation of the geographic location."""

    def __init__(self, *, data: SafetyMonitorDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")

        self.is_safe = data.get("IsSafe")
        self.supported_actions = data.get("SupportedActions")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.device_id = data.get("DeviceId")


# #########################################################################
# Switch
# #########################################################################
class SwitchPortDataModel(TypedDict, total=False):
    # device_list_response_item

    Name: str
    Description: str
    Id: int
    Maximum: Optional[int]
    Minimum: Optional[int]
    StepSize: Optional[int]
    TargetValue: Optional[int]
    Value: float


@typechecked
class SwitchPortData:
    """A representation of the geographic location."""

    def __init__(self, *, data: SwitchPortDataModel):
        self.name = data.get("Name")
        self.description = data.get("Description")
        self.id = data.get("Id")
        self.maximum = data.get("Maximum")
        self.minimum = data.get("Minimum")
        self.step_size = data.get("StepSize")
        self.target_value = data.get("TargetValue")
        self.value = data.get("Value")


class SwitchDataModel(TypedDict, total=False):
    # device_list_response_item

    Connected: bool
    Name: str
    DisplayName: str
    Description: str
    DeviceId: str
    DriverInfo: str
    DriverVersion: str
    ReadonlySwitches: Optional[list[SwitchPortDataModel]]
    SupportedActions: list[str]
    WritableSwitches: Optional[list[SwitchPortDataModel]]


@typechecked
class SwitchData:
    """A representation of the geographic location."""

    def __init__(self, *, data: SwitchDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.device_id = data.get("DeviceId")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.readonly_switches = data.get("ReadonlySwitches")
        self.supported_actions = data.get("SupportedActions")
        self.writable_switches = data.get("WritableSwitches")


# #########################################################################
# Weather
# #########################################################################
class WeatherDataModel(TypedDict, total=False):
    # device_list_response_item

    Connected: bool
    Name: str
    DisplayName: str
    Description: str

    AveragePeriod: int
    CloudCover: int
    DewPoint: float
    Humidity: int
    Pressure: float
    RainRate: float
    SkyBrightness: str
    SkyQuality: str
    SkyTemperature: str
    StarFWHM: str
    Temperature: float
    WindDirection: int
    WindGust: float
    WindSpeed: float
    SupportedActions: list[str]
    DriverInfo: str
    DriverVersion: str
    DeviceId: str


@typechecked
class WeatherData:
    """A representation of the geographic location."""

    def __init__(self, *, data: WeatherDataModel):
        self.connected = data.get("Connected")
        self.name = data.get("Name")
        self.display_name = data.get("DisplayName")
        self.description = data.get("Description")
        self.average_period = data.get("AveragePeriod")
        self.cloud_cover = data.get("CloudCover")
        self.dew_point = round(data.get("DewPoint"), 1) if data.get("DewPoint") is not None else None
        self.humidity = data.get("Humidity")
        self.pressure = round(data.get("Pressure"), 1) if data.get("Pressure") is not None else None
        self.rain_rate = round(data.get("RainRate"), 1) if data.get("RainRate") is not None else None
        self.sky_brightness = data.get("SkyBrightness")
        self.sky_quality = data.get("SkyQuality")
        self.sky_temperature = data.get("SkyTemperature")
        self.star_fwhm = data.get("StarFWHM")
        self.temperature = round(data.get("Temperature"), 1) if data.get("Temperature") is not None else None
        self.wind_direction = data.get("WindDirection")
        self.wind_gust = round(data.get("WindGust"), 1) if data.get("WindGust") is not None else None
        self.wind_speed = round(data.get("WindSpeed"), 1) if data.get("WindSpeed") is not None else None
        self.supported_actions = data.get("SupportedActions")
        self.driver_info = data.get("DriverInfo")
        self.driver_version = data.get("DriverVersion")
        self.device_id = data.get("DeviceId")


# #########################################################################
# N.I.N.A. Devices
# #########################################################################
class NinaDevicesDataModel(TypedDict, total=False):
    # device_list_response_item

    Connected: bool
    Application: Optional[ApplicationData]
    Camera: Optional[CameraData]
    Dome: Optional[DomeData]
    FilterWheel: Optional[FilterWheelData]
    # FlatPanel: Optional[FlatPanelData]
    Focuser: Optional[FocuserData]
    Guider: Optional[GuiderData]
    Image: Optional[ImageData]
    Mount: Optional[MountData]
    # Profile: Optional[ProfileData]
    Rotator: Optional[RotatorData]
    SafetyMonitor: Optional[SafetyMonitorData]
    # Sequence: Optional[SequenceData]
    Switch: Optional[SwitchData]
    Weather: Optional[WeatherData]


@typechecked
class NinaDevicesData:
    """A representation of the geographic location."""

    def __init__(self, *, data: NinaDevicesDataModel):
        self.connected = data.get("Connected")
        self.application = data.get("Application")
        self.camera = data.get("Camera")
        self.dome = data.get("Dome")
        self.filterwheel = data.get("FilterWheel")
        self.focuser = data.get("Focuser")
        self.guider = data.get("Guider")
        self.image = data.get("Image")
        self.mount = data.get("Mount")
        self.rotator = data.get("Rotator")
        self.safety_monitor = data.get("SafetyMonitor")
        self.switch = data.get("Switch")
        self.weather = data.get("Weather")
