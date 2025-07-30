from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ack import Ack
from ...types import UNSET, Response


def _get_kwargs(
    username: str,
    *,
    group_name: list[str],
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_group_name = group_name

    params["groupName"] = json_group_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/users/{username}/groups".format(
            username=username,
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
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: list[str],
) -> Response[Union[Ack, Any]]:
    """Remove user from groups

    Args:
        username (str):
        group_name (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        username=username,
        group_name=group_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: list[str],
) -> Optional[Union[Ack, Any]]:
    """Remove user from groups

    Args:
        username (str):
        group_name (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
    """

    return sync_detailed(
        username=username,
        client=client,
        group_name=group_name,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: list[str],
) -> Response[Union[Ack, Any]]:
    """Remove user from groups

    Args:
        username (str):
        group_name (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        username=username,
        group_name=group_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: list[str],
) -> Optional[Union[Ack, Any]]:
    """Remove user from groups

    Args:
        username (str):
        group_name (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            group_name=group_name,
        )
    ).parsed
