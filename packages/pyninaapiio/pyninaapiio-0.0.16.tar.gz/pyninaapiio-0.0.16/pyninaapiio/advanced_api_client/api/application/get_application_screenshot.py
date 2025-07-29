from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_application_screenshot_response_200 import GetApplicationScreenshotResponse200
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    resize: Union[Unset, bool] = UNSET,
    quality: Union[Unset, int] = UNSET,
    size: Union[Unset, str] = UNSET,
    scale: Union[Unset, float] = UNSET,
    stream: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["resize"] = resize

    params["quality"] = quality

    params["size"] = size

    params["scale"] = scale

    params["stream"] = stream

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/application/screenshot",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetApplicationScreenshotResponse200, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetApplicationScreenshotResponse200.from_dict(response.json())

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
) -> Response[Union[GetApplicationScreenshotResponse200, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    resize: Union[Unset, bool] = UNSET,
    quality: Union[Unset, int] = UNSET,
    size: Union[Unset, str] = UNSET,
    scale: Union[Unset, float] = UNSET,
    stream: Union[Unset, bool] = UNSET,
) -> Response[Union[GetApplicationScreenshotResponse200, UnknownError]]:
    """Screenshot

     Takes a screenshot

    Args:
        resize (Union[Unset, bool]):
        quality (Union[Unset, int]):
        size (Union[Unset, str]):
        scale (Union[Unset, float]):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetApplicationScreenshotResponse200, UnknownError]]
    """

    kwargs = _get_kwargs(
        resize=resize,
        quality=quality,
        size=size,
        scale=scale,
        stream=stream,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    resize: Union[Unset, bool] = UNSET,
    quality: Union[Unset, int] = UNSET,
    size: Union[Unset, str] = UNSET,
    scale: Union[Unset, float] = UNSET,
    stream: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetApplicationScreenshotResponse200, UnknownError]]:
    """Screenshot

     Takes a screenshot

    Args:
        resize (Union[Unset, bool]):
        quality (Union[Unset, int]):
        size (Union[Unset, str]):
        scale (Union[Unset, float]):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetApplicationScreenshotResponse200, UnknownError]
    """

    return sync_detailed(
        client=client,
        resize=resize,
        quality=quality,
        size=size,
        scale=scale,
        stream=stream,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    resize: Union[Unset, bool] = UNSET,
    quality: Union[Unset, int] = UNSET,
    size: Union[Unset, str] = UNSET,
    scale: Union[Unset, float] = UNSET,
    stream: Union[Unset, bool] = UNSET,
) -> Response[Union[GetApplicationScreenshotResponse200, UnknownError]]:
    """Screenshot

     Takes a screenshot

    Args:
        resize (Union[Unset, bool]):
        quality (Union[Unset, int]):
        size (Union[Unset, str]):
        scale (Union[Unset, float]):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetApplicationScreenshotResponse200, UnknownError]]
    """

    kwargs = _get_kwargs(
        resize=resize,
        quality=quality,
        size=size,
        scale=scale,
        stream=stream,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    resize: Union[Unset, bool] = UNSET,
    quality: Union[Unset, int] = UNSET,
    size: Union[Unset, str] = UNSET,
    scale: Union[Unset, float] = UNSET,
    stream: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetApplicationScreenshotResponse200, UnknownError]]:
    """Screenshot

     Takes a screenshot

    Args:
        resize (Union[Unset, bool]):
        quality (Union[Unset, int]):
        size (Union[Unset, str]):
        scale (Union[Unset, float]):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetApplicationScreenshotResponse200, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            resize=resize,
            quality=quality,
            size=size,
            scale=scale,
            stream=stream,
        )
    ).parsed
