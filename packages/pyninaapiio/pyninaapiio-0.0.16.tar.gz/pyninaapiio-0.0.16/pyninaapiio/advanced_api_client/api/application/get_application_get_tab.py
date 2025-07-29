from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_application_get_tab_response_200 import GetApplicationGetTabResponse200
from ...models.get_application_get_tab_response_400 import GetApplicationGetTabResponse400
from ...models.unknown_error import UnknownError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/application/get-tab",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetApplicationGetTabResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = GetApplicationGetTabResponse400.from_dict(response.json())

        return response_400
    if response.status_code == 500:
        response_500 = UnknownError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]:
    """Get Tab

     Gets the current application tab

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]:
    """Get Tab

     Gets the current application tab

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]:
    """Get Tab

     Gets the current application tab

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]]:
    """Get Tab

     Gets the current application tab

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetApplicationGetTabResponse200, GetApplicationGetTabResponse400, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
