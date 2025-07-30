from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_favorite_theme_scope import GetFavoriteThemeScope
from ...models.theme import Theme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    scope: Union[Unset, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_scope: Union[Unset, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params["groupName"] = group_name

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/themes/_favorite",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Theme]:
    if response.status_code == 200:
        response_200 = Theme.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Theme]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    scope: Union[Unset, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, GetFavoriteThemeScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Theme]
    """

    kwargs = _get_kwargs(
        scope=scope,
        group_name=group_name,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    scope: Union[Unset, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, GetFavoriteThemeScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Theme
    """

    return sync_detailed(
        client=client,
        scope=scope,
        group_name=group_name,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    scope: Union[Unset, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, GetFavoriteThemeScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Theme]
    """

    kwargs = _get_kwargs(
        scope=scope,
        group_name=group_name,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    scope: Union[Unset, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, GetFavoriteThemeScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Theme
    """

    return (
        await asyncio_detailed(
            client=client,
            scope=scope,
            group_name=group_name,
            username=username,
        )
    ).parsed
