from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_sequence_start_response_200 import GetSequenceStartResponse200
from ...models.get_sequence_start_response_409 import GetSequenceStartResponse409
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    skip_validation: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["skipValidation"] = skip_validation

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sequence/start",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetSequenceStartResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = GetSequenceStartResponse409.from_dict(response.json())

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
) -> Response[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip_validation: Union[Unset, bool] = UNSET,
) -> Response[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]:
    """Start

     Start sequence. This requires the sequencer to be initalized, which can be achieved by opening the
    tab once.

    Args:
        skip_validation (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        skip_validation=skip_validation,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    skip_validation: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]:
    """Start

     Start sequence. This requires the sequencer to be initalized, which can be achieved by opening the
    tab once.

    Args:
        skip_validation (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]
    """

    return sync_detailed(
        client=client,
        skip_validation=skip_validation,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip_validation: Union[Unset, bool] = UNSET,
) -> Response[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]:
    """Start

     Start sequence. This requires the sequencer to be initalized, which can be achieved by opening the
    tab once.

    Args:
        skip_validation (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        skip_validation=skip_validation,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip_validation: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]]:
    """Start

     Start sequence. This requires the sequencer to be initalized, which can be achieved by opening the
    tab once.

    Args:
        skip_validation (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSequenceStartResponse200, GetSequenceStartResponse409, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip_validation=skip_validation,
        )
    ).parsed
