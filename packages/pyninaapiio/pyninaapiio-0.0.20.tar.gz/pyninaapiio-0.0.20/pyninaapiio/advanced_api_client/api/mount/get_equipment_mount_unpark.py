from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_equipment_mount_unpark_response_200 import GetEquipmentMountUnparkResponse200
from ...models.get_equipment_mount_unpark_response_409 import GetEquipmentMountUnparkResponse409
from ...models.unknown_error import UnknownError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/equipment/mount/unpark",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetEquipmentMountUnparkResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = GetEquipmentMountUnparkResponse409.from_dict(response.json())

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
) -> Response[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]:
    """Unpark

     Unpark the mount

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]:
    """Unpark

     Unpark the mount

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]:
    """Unpark

     Unpark the mount

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]]:
    """Unpark

     Unpark the mount

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentMountUnparkResponse200, GetEquipmentMountUnparkResponse409, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
