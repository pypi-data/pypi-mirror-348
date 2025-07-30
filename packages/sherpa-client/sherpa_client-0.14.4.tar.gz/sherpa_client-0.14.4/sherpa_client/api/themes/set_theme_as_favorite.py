from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.ack import Ack
from ...models.set_theme_as_favorite_scope import SetThemeAsFavoriteScope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    theme_id: str,
    *,
    client: Client,
    favorite: bool,
    scope: Union[Unset, None, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/themes/{themeId}/_favorite".format(client.base_url, themeId=theme_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["favorite"] = favorite

    json_scope: Union[Unset, None, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value if scope else None

    params["scope"] = json_scope

    params["groupName"] = group_name

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Ack, Any]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Ack.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Ack, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    theme_id: str,
    *,
    client: Client,
    favorite: bool,
    scope: Union[Unset, None, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, None, SetThemeAsFavoriteScope]):  Default:
            SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        theme_id=theme_id,
        client=client,
        favorite=favorite,
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
    theme_id: str,
    *,
    client: Client,
    favorite: bool,
    scope: Union[Unset, None, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, None, SetThemeAsFavoriteScope]):  Default:
            SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return sync_detailed(
        theme_id=theme_id,
        client=client,
        favorite=favorite,
        scope=scope,
        group_name=group_name,
        username=username,
    ).parsed


async def asyncio_detailed(
    theme_id: str,
    *,
    client: Client,
    favorite: bool,
    scope: Union[Unset, None, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, None, SetThemeAsFavoriteScope]):  Default:
            SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        theme_id=theme_id,
        client=client,
        favorite=favorite,
        scope=scope,
        group_name=group_name,
        username=username,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    theme_id: str,
    *,
    client: Client,
    favorite: bool,
    scope: Union[Unset, None, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, None, str] = UNSET,
    username: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, None, SetThemeAsFavoriteScope]):  Default:
            SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, None, str]):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return (
        await asyncio_detailed(
            theme_id=theme_id,
            client=client,
            favorite=favorite,
            scope=scope,
            group_name=group_name,
            username=username,
        )
    ).parsed
