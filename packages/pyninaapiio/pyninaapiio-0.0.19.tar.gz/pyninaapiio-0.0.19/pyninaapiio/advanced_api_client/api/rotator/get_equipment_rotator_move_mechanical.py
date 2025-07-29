from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_equipment_rotator_move_mechanical_response_200 import GetEquipmentRotatorMoveMechanicalResponse200
from ...models.get_equipment_rotator_move_mechanical_response_409 import GetEquipmentRotatorMoveMechanicalResponse409
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    position: float,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["position"] = position

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/equipment/rotator/move-mechanical",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
]:
    if response.status_code == 200:
        response_200 = GetEquipmentRotatorMoveMechanicalResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = GetEquipmentRotatorMoveMechanicalResponse409.from_dict(response.json())

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
) -> Response[
    Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    position: float,
) -> Response[
    Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
]:
    """Move Mechanically

     Move the rotator mechanically

    Args:
        position (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        position=position,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    position: float,
) -> Optional[
    Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
]:
    """Move Mechanically

     Move the rotator mechanically

    Args:
        position (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
    """

    return sync_detailed(
        client=client,
        position=position,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    position: float,
) -> Response[
    Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
]:
    """Move Mechanically

     Move the rotator mechanically

    Args:
        position (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        position=position,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    position: float,
) -> Optional[
    Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
]:
    """Move Mechanically

     Move the rotator mechanically

    Args:
        position (float):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEquipmentRotatorMoveMechanicalResponse200, GetEquipmentRotatorMoveMechanicalResponse409, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            position=position,
        )
    ).parsed
