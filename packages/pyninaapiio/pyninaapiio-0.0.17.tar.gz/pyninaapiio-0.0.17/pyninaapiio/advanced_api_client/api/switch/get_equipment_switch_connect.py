from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_equipment_switch_connect_response_200 import GetEquipmentSwitchConnectResponse200
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    to: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["to"] = to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/equipment/switch/connect",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetEquipmentSwitchConnectResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 500:
        response_500 = UnknownError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    to: Union[Unset, str] = UNSET,
) -> Response[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]:
    """Connect

     Connect to Switch

    Args:
        to (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]
    """

    kwargs = _get_kwargs(
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    to: Union[Unset, str] = UNSET,
) -> Optional[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]:
    """Connect

     Connect to Switch

    Args:
        to (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentSwitchConnectResponse200, UnknownError]
    """

    return sync_detailed(
        client=client,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    to: Union[Unset, str] = UNSET,
) -> Response[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]:
    """Connect

     Connect to Switch

    Args:
        to (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]
    """

    kwargs = _get_kwargs(
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    to: Union[Unset, str] = UNSET,
) -> Optional[Union[GetEquipmentSwitchConnectResponse200, UnknownError]]:
    """Connect

     Connect to Switch

    Args:
        to (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentSwitchConnectResponse200, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            to=to,
        )
    ).parsed
