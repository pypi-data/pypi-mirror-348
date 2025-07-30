from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_livestack_target_filter_response_200 import GetLivestackTargetFilterResponse200
from ...models.unknown_error import UnknownError
from ...types import Response


def _get_kwargs(
    target: str,
    filter_: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/livestack/{target}/{filter_}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetLivestackTargetFilterResponse200, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetLivestackTargetFilterResponse200.from_dict(response.json())

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
) -> Response[Union[GetLivestackTargetFilterResponse200, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    target: str,
    filter_: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetLivestackTargetFilterResponse200, UnknownError]]:
    """Get Stacked Image

     Gets the stacked image from the livestack plugin for a given target and filter.

    Args:
        target (str):  Example: M31.
        filter_ (str):  Example: RGB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetLivestackTargetFilterResponse200, UnknownError]]
    """

    kwargs = _get_kwargs(
        target=target,
        filter_=filter_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    target: str,
    filter_: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetLivestackTargetFilterResponse200, UnknownError]]:
    """Get Stacked Image

     Gets the stacked image from the livestack plugin for a given target and filter.

    Args:
        target (str):  Example: M31.
        filter_ (str):  Example: RGB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetLivestackTargetFilterResponse200, UnknownError]
    """

    return sync_detailed(
        target=target,
        filter_=filter_,
        client=client,
    ).parsed


async def asyncio_detailed(
    target: str,
    filter_: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetLivestackTargetFilterResponse200, UnknownError]]:
    """Get Stacked Image

     Gets the stacked image from the livestack plugin for a given target and filter.

    Args:
        target (str):  Example: M31.
        filter_ (str):  Example: RGB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetLivestackTargetFilterResponse200, UnknownError]]
    """

    kwargs = _get_kwargs(
        target=target,
        filter_=filter_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    target: str,
    filter_: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetLivestackTargetFilterResponse200, UnknownError]]:
    """Get Stacked Image

     Gets the stacked image from the livestack plugin for a given target and filter.

    Args:
        target (str):  Example: M31.
        filter_ (str):  Example: RGB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetLivestackTargetFilterResponse200, UnknownError]
    """

    return (
        await asyncio_detailed(
            target=target,
            filter_=filter_,
            client=client,
        )
    ).parsed
