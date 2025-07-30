from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_themes_scope import GetThemesScope
from ...models.theme import Theme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    scope: Union[Unset, GetThemesScope] = UNSET,
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
        "url": "/themes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Theme"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_theme_array_item_data in _response_200:
            componentsschemas_theme_array_item = Theme.from_dict(
                componentsschemas_theme_array_item_data
            )

            response_200.append(componentsschemas_theme_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Theme"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    scope: Union[Unset, GetThemesScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["Theme"]]:
    """Get UI themes

    Args:
        scope (Union[Unset, GetThemesScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Theme']]
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
    scope: Union[Unset, GetThemesScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[list["Theme"]]:
    """Get UI themes

    Args:
        scope (Union[Unset, GetThemesScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Theme']
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
    scope: Union[Unset, GetThemesScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["Theme"]]:
    """Get UI themes

    Args:
        scope (Union[Unset, GetThemesScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Theme']]
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
    scope: Union[Unset, GetThemesScope] = UNSET,
    group_name: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[list["Theme"]]:
    """Get UI themes

    Args:
        scope (Union[Unset, GetThemesScope]):
        group_name (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Theme']
    """

    return (
        await asyncio_detailed(
            client=client,
            scope=scope,
            group_name=group_name,
            username=username,
        )
    ).parsed
