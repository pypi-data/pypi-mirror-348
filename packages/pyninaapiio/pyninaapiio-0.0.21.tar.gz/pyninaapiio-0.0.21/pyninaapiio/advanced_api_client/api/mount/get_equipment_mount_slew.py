from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_equipment_mount_slew_response_200 import GetEquipmentMountSlewResponse200
from ...models.get_equipment_mount_slew_response_409 import GetEquipmentMountSlewResponse409
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    ra: float,
    dec: float,
    wait_for_result: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ra"] = ra

    params["dec"] = dec

    params["waitForResult"] = wait_for_result

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/equipment/mount/slew",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetEquipmentMountSlewResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = GetEquipmentMountSlewResponse409.from_dict(response.json())

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
) -> Response[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ra: float,
    dec: float,
    wait_for_result: Union[Unset, bool] = UNSET,
) -> Response[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]:
    """Slew

     Performs a slew to the provided coordinates

    Args:
        ra (float):
        dec (float):
        wait_for_result (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        ra=ra,
        dec=dec,
        wait_for_result=wait_for_result,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    ra: float,
    dec: float,
    wait_for_result: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]:
    """Slew

     Performs a slew to the provided coordinates

    Args:
        ra (float):
        dec (float):
        wait_for_result (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]
    """

    return sync_detailed(
        client=client,
        ra=ra,
        dec=dec,
        wait_for_result=wait_for_result,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ra: float,
    dec: float,
    wait_for_result: Union[Unset, bool] = UNSET,
) -> Response[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]:
    """Slew

     Performs a slew to the provided coordinates

    Args:
        ra (float):
        dec (float):
        wait_for_result (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        ra=ra,
        dec=dec,
        wait_for_result=wait_for_result,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    ra: float,
    dec: float,
    wait_for_result: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]]:
    """Slew

     Performs a slew to the provided coordinates

    Args:
        ra (float):
        dec (float):
        wait_for_result (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentMountSlewResponse200, GetEquipmentMountSlewResponse409, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            ra=ra,
            dec=dec,
            wait_for_result=wait_for_result,
        )
    ).parsed
