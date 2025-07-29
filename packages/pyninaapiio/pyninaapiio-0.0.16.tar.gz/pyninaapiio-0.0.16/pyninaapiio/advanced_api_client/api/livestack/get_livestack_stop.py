from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_livestack_stop_response_200 import GetLivestackStopResponse200
from ...models.unknown_error import UnknownError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/livestack/stop",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetLivestackStopResponse200, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetLivestackStopResponse200.from_dict(response.json())

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
) -> Response[Union[GetLivestackStopResponse200, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetLivestackStopResponse200, UnknownError]]:
    """Stop Livestack

     Stops Livestack, requires Livestack >= v1.0.0.9. Note that this method cannot fail, even if the
    livestack plugin is not installed or something went wrong. This simply issues a command to stop the
    livestack.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetLivestackStopResponse200, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetLivestackStopResponse200, UnknownError]]:
    """Stop Livestack

     Stops Livestack, requires Livestack >= v1.0.0.9. Note that this method cannot fail, even if the
    livestack plugin is not installed or something went wrong. This simply issues a command to stop the
    livestack.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetLivestackStopResponse200, UnknownError]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetLivestackStopResponse200, UnknownError]]:
    """Stop Livestack

     Stops Livestack, requires Livestack >= v1.0.0.9. Note that this method cannot fail, even if the
    livestack plugin is not installed or something went wrong. This simply issues a command to stop the
    livestack.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetLivestackStopResponse200, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetLivestackStopResponse200, UnknownError]]:
    """Stop Livestack

     Stops Livestack, requires Livestack >= v1.0.0.9. Note that this method cannot fail, even if the
    livestack plugin is not installed or something went wrong. This simply issues a command to stop the
    livestack.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetLivestackStopResponse200, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
