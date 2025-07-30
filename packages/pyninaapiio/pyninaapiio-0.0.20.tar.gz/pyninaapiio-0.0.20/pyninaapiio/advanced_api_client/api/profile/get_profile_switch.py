from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_profile_switch_response_200 import GetProfileSwitchResponse200
from ...models.get_profile_switch_response_409 import GetProfileSwitchResponse409
from ...models.unknown_error import UnknownError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    profileid: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["profileid"] = profileid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/profile/switch",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]:
    if response.status_code == 200:
        response_200 = GetProfileSwitchResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = GetProfileSwitchResponse409.from_dict(response.json())

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
) -> Response[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    profileid: str,
) -> Response[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]:
    """Switch Profile

     Switches the profile

    Args:
        profileid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        profileid=profileid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    profileid: str,
) -> Optional[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]:
    """Switch Profile

     Switches the profile

    Args:
        profileid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]
    """

    return sync_detailed(
        client=client,
        profileid=profileid,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    profileid: str,
) -> Response[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]:
    """Switch Profile

     Switches the profile

    Args:
        profileid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]
    """

    kwargs = _get_kwargs(
        profileid=profileid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    profileid: str,
) -> Optional[Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]]:
    """Switch Profile

     Switches the profile

    Args:
        profileid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetProfileSwitchResponse200, GetProfileSwitchResponse409, UnknownError]
    """

    return (
        await asyncio_detailed(
            client=client,
            profileid=profileid,
        )
    ).parsed
