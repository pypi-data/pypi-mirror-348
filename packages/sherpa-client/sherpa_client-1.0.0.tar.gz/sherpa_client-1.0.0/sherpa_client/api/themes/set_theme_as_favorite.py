from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ack import Ack
from ...models.set_theme_as_favorite_scope import SetThemeAsFavoriteScope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    theme_id: str,
    *,
    favorite: bool,
    scope: Union[Unset, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["favorite"] = favorite

    json_scope: Union[Unset, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params["groupName"] = group_name

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/themes/{theme_id}/_favorite".format(
            theme_id=theme_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Ack, Any]]:
    if response.status_code == 200:
        response_200 = Ack.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Ack, Any]]:
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
    favorite: bool,
    scope: Union[Unset, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, SetThemeAsFavoriteScope]):  Default: SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        theme_id=theme_id,
        favorite=favorite,
        scope=scope,
        group_name=group_name,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    theme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    favorite: bool,
    scope: Union[Unset, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, SetThemeAsFavoriteScope]):  Default: SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
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
    client: Union[AuthenticatedClient, Client],
    favorite: bool,
    scope: Union[Unset, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, SetThemeAsFavoriteScope]):  Default: SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        theme_id=theme_id,
        favorite=favorite,
        scope=scope,
        group_name=group_name,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    theme_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    favorite: bool,
    scope: Union[Unset, SetThemeAsFavoriteScope] = SetThemeAsFavoriteScope.USER,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Set a UI theme as favorite

    Args:
        theme_id (str):
        favorite (bool):
        scope (Union[Unset, SetThemeAsFavoriteScope]):  Default: SetThemeAsFavoriteScope.USER.
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
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
