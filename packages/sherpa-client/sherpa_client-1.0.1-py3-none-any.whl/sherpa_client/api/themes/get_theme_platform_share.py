from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.platform_share import PlatformShare
from ...types import Response


def _get_kwargs(
    theme_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/themes/{theme_id}/shares/platform".format(
            theme_id=theme_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["PlatformShare"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_platform_share_array_item_data in _response_200:
            componentsschemas_platform_share_array_item = PlatformShare.from_dict(
                componentsschemas_platform_share_array_item_data
            )

            response_200.append(componentsschemas_platform_share_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PlatformShare"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    theme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["PlatformShare"]]:
    """Get share with platform

    Args:
        theme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PlatformShare']]
    """

    kwargs = _get_kwargs(
        theme_id=theme_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    theme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list["PlatformShare"]]:
    """Get share with platform

    Args:
        theme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PlatformShare']
    """

    return sync_detailed(
        theme_id=theme_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    theme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["PlatformShare"]]:
    """Get share with platform

    Args:
        theme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PlatformShare']]
    """

    kwargs = _get_kwargs(
        theme_id=theme_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    theme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[list["PlatformShare"]]:
    """Get share with platform

    Args:
        theme_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PlatformShare']
    """

    return (
        await asyncio_detailed(
            theme_id=theme_id,
            client=client,
        )
    ).parsed
