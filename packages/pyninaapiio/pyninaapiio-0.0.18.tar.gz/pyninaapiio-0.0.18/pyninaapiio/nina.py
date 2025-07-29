import base64
import logging
import sys
import traceback
from pprint import pprint as pp

from httpx import ConnectError, ConnectTimeout, ReadTimeout
from typeguard import TypeCheckError

from .advanced_api_client.api.application import get_version
from .advanced_api_client.api.camera import get_equipment_camera_info
from .advanced_api_client.api.dome import get_equipment_dome_info
from .advanced_api_client.api.filter_wheel import get_equipment_filterwheel_info
from .advanced_api_client.api.focuser import get_equipment_focuser_info
from .advanced_api_client.api.guider import get_equipment_guider_info
from .advanced_api_client.api.image import get_image_history, get_image_index
from .advanced_api_client.api.mount import get_equipment_mount_info, get_equipment_mount_list_devices
from .advanced_api_client.api.rotator import get_equipment_rotator_info
from .advanced_api_client.api.safety_monitor import get_equipment_safetymonitor_info
from .advanced_api_client.api.switch import get_equipment_switch_info
from .advanced_api_client.api.weather import get_equipment_weather_info
from .advanced_api_client.client import Client
from .advanced_api_client.models.camera_info import CameraInfo
from .advanced_api_client.models.device_list import DeviceList
from .advanced_api_client.models.focuser_info import FocuserInfo
from .advanced_api_client.models.fw_info import FWInfo
from .advanced_api_client.models.get_image_history_response_200 import GetImageHistoryResponse200
from .advanced_api_client.models.get_image_index_bayer_pattern import GetImageIndexBayerPattern
from .advanced_api_client.models.get_image_index_response_200 import GetImageIndexResponse200
from .advanced_api_client.models.get_version_response_200 import GetVersionResponse200
from .advanced_api_client.models.guider_info import GuiderInfo
from .advanced_api_client.models.mount_info import MountInfo
from .advanced_api_client.models.rotator_info import RotatorInfo
from .advanced_api_client.models.safety_monitor_info import SafetyMonitorInfo
from .advanced_api_client.models.switch_info import SwitchInfo
from .advanced_api_client.models.weather_info import WeatherInfo
from .advanced_api_client.types import Response
from .dataclasses import (
    ApplicationData,
    ApplicationDataModel,
    CameraData,
    CameraDataModel,
    DomeData,
    DomeDataModel,
    FilterWheelData,
    FilterWheelDataModel,
    FocuserData,
    FocuserDataModel,
    GuiderData,
    GuiderDataModel,
    ImageData,
    ImageDataModel,
    MountData,
    MountDataModel,
    NinaDevicesData,
    NinaDevicesDataModel,
    RotatorData,
    RotatorDataModel,
    SafetyMonitorData,
    SafetyMonitorDataModel,
    SwitchData,
    SwitchDataModel,
    WeatherData,
    WeatherDataModel,
)

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s (%(threadName)s) [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DEFAULT_API_TIMEOUT = 10


# async with client as client:
class NinaAPI:
    def __init__(
        self,
        # session: Optional[ClientSession] = None,
        session=None,
        base_url="http://192.168.1.234:1888/v2/api",
        application_enabled=False,
        camera_enabled=False,
        dome_enabled=False,
        filterwheel_enabled=False,
        focuser_enabled=False,
        guider_enabled=False,
        image_enabled=False,
        mount_enabled=False,
        rotator_enabled=False,
        safety_monitor_enabled=False,
        switch_enabled=False,
        weather_enabled=False,
        api_timeout=DEFAULT_API_TIMEOUT,
    ):
        self._session = session
        self._client = Client(base_url=base_url, timeout=api_timeout, verify_ssl=False)
        self._application_enabled = application_enabled
        self._camera_enabled = camera_enabled
        self._dome_enabled = dome_enabled
        self._filterwheel_enabled = filterwheel_enabled
        self._focuser_enabled = focuser_enabled
        self._guider_enabled = guider_enabled
        self._image_enabled = image_enabled
        self._mount_enabled = mount_enabled
        self._rotator_enabled = rotator_enabled
        self._safety_monitor_enabled = safety_monitor_enabled
        self._switch_enabled = switch_enabled
        self._weather_enabled = weather_enabled

        # Save last capture
        self._image_index_latest = -1
        self._image_data = b""
        self._image_details_data = {}

        return None

    # #########################################################################
    # Application
    # #########################################################################
    async def application_info(self):
        try:
            _LOGGER.debug("Retrieve info: Application")
            _application_info: Response[GetVersionResponse200] = await get_version.asyncio(client=self._client)
            _application_info_data = ApplicationDataModel({"Version": _application_info.response, "Connected": True})

            return ApplicationData(data=_application_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return ApplicationData(data={"Connected": False})
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Application not connected.")
            return ApplicationData(data={"Connected": False})

    # #########################################################################
    # Camera
    # #########################################################################
    async def camera_info(self):
        try:
            _LOGGER.debug("Retrieve info: Camera")
            _camera_info: Response[CameraInfo] = await get_equipment_camera_info.asyncio(client=self._client)
            _camera_info_data = CameraDataModel(_camera_info.response.to_dict())
            # print(_camera_info_data)
            return CameraData(data=_camera_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Camera not connected.")
            return CameraData(data={"Connected": False})

    # #########################################################################
    # Dome
    # #########################################################################
    async def dome_info(self):
        try:
            _LOGGER.debug("Retrieve info: Filterwheel")
            _dome_info: Response[FWInfo] = await get_equipment_dome_info.asyncio(client=self._client)
            _dome_info_data = DomeDataModel(_dome_info.response.to_dict())

            return DomeData(data=_dome_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Dome not connected.")
            return DomeData(data={"Connected": False})

    # #########################################################################
    # FilterWheel
    # #########################################################################
    async def filterwheel_info(self):
        try:
            _LOGGER.debug("Retrieve info: Filterwheel")
            _filterwheel_info: Response[FWInfo] = await get_equipment_filterwheel_info.asyncio(client=self._client)
            _filterwheel_info_data = FilterWheelDataModel(_filterwheel_info.response.to_dict())

            return FilterWheelData(data=_filterwheel_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("FilterWheel not connected.")
            return FilterWheelData(data={"Connected": False})

    # #########################################################################
    # Focuser
    # #########################################################################
    async def focuser_info(self):
        try:
            _LOGGER.debug("Retrieve info: Focuser")
            _focuser_info: Response[FocuserInfo] = await get_equipment_focuser_info.asyncio(client=self._client)
            _focuser_info_data = FocuserDataModel(_focuser_info.response.to_dict())

            return FocuserData(data=_focuser_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Focuser not connected.")
            return FocuserData(data={"Connected": False})

    # #########################################################################
    # Guider
    # #########################################################################
    async def guider_info(self):
        try:
            _LOGGER.debug("Retrieve info: Guider")
            _guider_info: Response[GuiderInfo] = await get_equipment_guider_info.asyncio(client=self._client)
            _guider_info_data = GuiderDataModel(_guider_info.response.to_dict())

            return GuiderData(data=_guider_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Guider not connected.")
            return GuiderData(data={"Connected": False})

    # #########################################################################
    # Image
    # #########################################################################
    async def image_latest(self):
        try:
            _LOGGER.debug("Retrieve index of last capture")
            image_history: GetImageHistoryResponse200 = await get_image_history.asyncio(client=self._client, count=True)
            image_index_latest = image_history.response - 1

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None

        if image_index_latest > self._image_index_latest:
            self._image_index_latest = image_index_latest

            try:
                _LOGGER.debug("Retrieve capture detail data")
                image_details: GetImageHistoryResponse200 = await get_image_history.asyncio(
                    client=self._client, index=image_index_latest
                )
                self._image_details_data = image_details.response[0].to_dict()
                # print(self._image_details_data)
                _LOGGER.debug(f"Retrieve capture with index {image_index_latest}")
                image: GetImageIndexResponse200 = await get_image_index.asyncio(
                    index=image_index_latest,
                    client=self._client,
                    debayer=self._image_details_data.get("IsBayered", False),
                    bayer_pattern=GetImageIndexBayerPattern.RGGB,
                    resize=True,
                    scale=0.5,
                    # auto_prepare=True,
                    # self._image_details_data.get("IsBayered", False),
                )
                if image.success:
                    image_data = base64.b64decode(image.response)
                    self._image_data = image_data
                else:
                    _LOGGER.error(f"{image.error}")
            except ReadTimeout as rt:
                _LOGGER.warning("Timeout retrieving capture. Try increasing the timeout.")
                return None
        else:
            _LOGGER.debug(f"Returning previous capture with index {self._image_index_latest}")

        _LOGGER.debug(f"Capture Index: {self._image_index_latest}")
        _camera_data = ImageDataModel(
            {
                "Connected": True,
                "DecodedData": self._image_data,
                "DecodedDataLength": len(self._image_data),
                "IndexLatest": self._image_index_latest,
            }
            | self._image_details_data
        )
        return ImageData(data=_camera_data)

    # #########################################################################
    # Mount
    # #########################################################################
    # async def mount_list_devices(self):
    #     items = []

    #     try:
    #         _list_devices: Response[DeviceList] = await get_equipment_mount_list_devices.asyncio(client=self._client)

    #         for _, device in enumerate(_list_devices.response):
    #             item = DeviceMountDataModel(device.to_dict())

    #             try:
    #                 items.append(DeviceMountData(data=item))
    #             except TypeError as ve:
    #                 _LOGGER.error(f"Failed to parse device data model data: {item}")
    #                 _LOGGER.error(ve)
    #     except KeyError as ke:
    #         _LOGGER.error(f"KeyError:")

    #     return items

    async def mount_info(self):
        try:
            _LOGGER.debug("Retrieve info: Mount")
            _mount_info: Response[MountInfo] = await get_equipment_mount_info.asyncio(client=self._client)
            _mount_info_data = MountDataModel(_mount_info.response.to_dict())

            return MountData(data=_mount_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Mount not connected.")
            return MountData(data={"Connected": False})

    # #########################################################################
    # Rotator
    # #########################################################################
    async def rotator_info(self):
        try:
            _LOGGER.debug("Retrieve inf: Rotator")
            _rotator_info: Response[RotatorInfo] = await get_equipment_rotator_info.asyncio(client=self._client)
            _rotator_info_data = RotatorDataModel(_rotator_info.response.to_dict())

            return RotatorData(data=_rotator_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Rotator not connected.")
            return RotatorData(data={"Connected": False})

    # #########################################################################
    # SafetyMonitor
    # #########################################################################
    async def safety_monitor_info(self):
        try:
            _LOGGER.debug("Retrieve inf: SafetyMonitor")
            _safety_monitor_info: Response[SafetyMonitorInfo] = await get_equipment_safetymonitor_info.asyncio(
                client=self._client
            )
            _safety_monitor_info_data = SafetyMonitorDataModel(_safety_monitor_info.response.to_dict())

            return SafetyMonitorData(data=_safety_monitor_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("SafetyMonitor not connected.")
            return SafetyMonitorData(data={"Connected": False})

    # #########################################################################
    # Switch
    # #########################################################################
    async def switch_info(self):
        try:
            _LOGGER.debug("Retrieve inf: Switch")
            _switch_info: Response[SwitchInfo] = await get_equipment_switch_info.asyncio(client=self._client)
            _switch_info_data = SwitchDataModel(_switch_info.response.to_dict())

            return SwitchData(data=_switch_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Switch not connected.")
            return SwitchData(data={"Connected": False})

    # #########################################################################
    # Weather
    # #########################################################################
    async def weather_info(self):
        try:
            _LOGGER.debug("Retrieve inf: Weather")
            _weather_info: Response[WeatherInfo] = await get_equipment_weather_info.asyncio(client=self._client)
            _weather_info_data = WeatherDataModel(_weather_info.response.to_dict())

            return WeatherData(data=_weather_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return None
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            _LOGGER.debug("Weather not connected.")
            return WeatherData(data={"Connected": False})

    # #########################################################################
    # N.I.N.A.
    # #########################################################################
    async def nina_info(
        self,
    ) -> NinaDevicesData:
        _LOGGER.debug("Connecting to N.I.N.A.")
        application_data: ApplicationData = await self.application_info()

        if application_data.connected is False:
            _LOGGER.warning("N.I.N.A. not available.")
            return NinaDevicesData(data={"Connected": False})

        try:
            _LOGGER.debug("Retrieve info: N.I.N.A.")
            _nina = {
                "Application": await self.application_info() if self._application_enabled else None,
                "Camera": await self.camera_info() if self._camera_enabled else None,
                "Dome": await self.dome_info() if self._dome_enabled else None,
                "FilterWheel": await self.filterwheel_info() if self._filterwheel_enabled else None,
                "Focuser": await self.focuser_info() if self._focuser_enabled else None,
                "Guider": await self.guider_info() if self._guider_enabled else None,
                "Image": await self.image_latest() if self._image_enabled else None,
                "Mount": await self.mount_info() if self._mount_enabled else None,
                "Rotator": await self.rotator_info() if self._rotator_enabled else None,
                "SafetyMonitor": await self.safety_monitor_info() if self._safety_monitor_enabled else None,
                "Switch": await self.switch_info() if self._switch_enabled else None,
                "Weather": await self.weather_info() if self._weather_enabled else None,
            }
            _nina_info_data = NinaDevicesDataModel(_nina)

            return NinaDevicesData(data=_nina_info_data)

        except ConnectError as ce:
            _LOGGER.warning("Astro server not available.")
            return ApplicationData(data={"Connected": False})
        except ConnectTimeout as ct:
            _LOGGER.warning("N.I.N.A. not available.")
            return NinaDevicesData(data={"Connected": False})
        except TypeCheckError as tce:
            _LOGGER.warning(f"TypeCheckError: {tce}")
            return None
        except KeyError as ke:
            # traceback.print_exc()
            _LOGGER.debug("N.I.N.A. not connected.")
            return NinaDevicesData(data={"Connected": False})
