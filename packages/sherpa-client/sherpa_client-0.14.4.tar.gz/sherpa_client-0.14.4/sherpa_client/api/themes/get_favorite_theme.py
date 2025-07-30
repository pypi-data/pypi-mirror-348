from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.get_favorite_theme_scope import GetFavoriteThemeScope
from ...models.theme import Theme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    scope: Union[Unset, None, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/themes/_favorite".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_scope: Union[Unset, None, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value if scope else None

    params["scope"] = json_scope

    params["groupName"] = group_name

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Theme]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Theme.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Theme]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    scope: Union[Unset, None, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Response[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, None, GetFavoriteThemeScope]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Theme]
    """

    kwargs = _get_kwargs(
        client=client,
        scope=scope,
        group_name=group_name,
        username=username,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    scope: Union[Unset, None, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Optional[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, None, GetFavoriteThemeScope]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Theme]
    """

    return sync_detailed(
        client=client,
        scope=scope,
        group_name=group_name,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    scope: Union[Unset, None, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Response[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, None, GetFavoriteThemeScope]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Theme]
    """

    kwargs = _get_kwargs(
        client=client,
        scope=scope,
        group_name=group_name,
        username=username,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    scope: Union[Unset, None, GetFavoriteThemeScope] = UNSET,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Optional[Theme]:
    """Get the favorite UI theme

    Args:
        scope (Union[Unset, None, GetFavoriteThemeScope]):
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Theme]
    """

    return (
        await asyncio_detailed(
            client=client,
            scope=scope,
            group_name=group_name,
            username=username,
        )
    ).parsed
