from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_sequence_list_available_response_200 import GetSequenceListAvailableResponse200
from ...models.unknown_error import UnknownError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sequence/list-available",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetSequenceListAvailableResponse200, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetSequenceListAvailableResponse200.from_dict(response.json())

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
) -> Response[Union[GetSequenceListAvailableResponse200, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetSequenceListAvailableResponse200, UnknownError]]:
    """Available Sequences

     List available sequences. This is currently not really useful as it is not possible to load
    sequences

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSequenceListAvailableResponse200, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetSequenceListAvailableResponse200, UnknownError]]:
    """Available Sequences

     List available sequences. This is currently not really useful as it is not possible to load
    sequences

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSequenceListAvailableResponse200, UnknownError]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetSequenceListAvailableResponse200, UnknownError]]:
    """Available Sequences

     List available sequences. This is currently not really useful as it is not possible to load
    sequences

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSequenceListAvailableResponse200, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetSequenceListAvailableResponse200, UnknownError]]:
    """Available Sequences

     List available sequences. This is currently not really useful as it is not possible to load
    sequences

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSequenceListAvailableResponse200, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
