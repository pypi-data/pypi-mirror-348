from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_equipment_camera_dew_heater_response_200 import GetEquipmentCameraDewHeaterResponse200
from ...models.get_equipment_camera_dew_heater_response_409 import GetEquipmentCameraDewHeaterResponse409
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    power: bool,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["power"] = power

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/equipment/camera/dew-heater",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetEquipmentCameraDewHeaterResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = GetEquipmentCameraDewHeaterResponse409.from_dict(response.json())

        return response_409
    if response.status_code == 500:
        response_500 = UnknownError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    power: bool,
) -> Response[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]:
    """Dew Heater Control

     This endpoint sets the dew heater.

    Args:
        power (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        power=power,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    power: bool,
) -> Optional[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]:
    """Dew Heater Control

     This endpoint sets the dew heater.

    Args:
        power (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]
    """

    return sync_detailed(
        client=client,
        power=power,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    power: bool,
) -> Response[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]:
    """Dew Heater Control

     This endpoint sets the dew heater.

    Args:
        power (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        power=power,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    power: bool,
) -> Optional[Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]]:
    """Dew Heater Control

     This endpoint sets the dew heater.

    Args:
        power (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentCameraDewHeaterResponse200, GetEquipmentCameraDewHeaterResponse409, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            power=power,
        )
    ).parsed
