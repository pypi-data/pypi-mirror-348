from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.users_response import UsersResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    group_name: Union[Unset, str] = UNSET,
    admin_data: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["groupName"] = group_name

    params["adminData"] = admin_data

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UsersResponse]:
    if response.status_code == 200:
        response_200 = UsersResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UsersResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: Union[Unset, str] = UNSET,
    admin_data: Union[Unset, bool] = False,
) -> Response[UsersResponse]:
    """Get users

    Args:
        group_name (Union[Unset, str]):
        admin_data (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsersResponse]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
        admin_data=admin_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: Union[Unset, str] = UNSET,
    admin_data: Union[Unset, bool] = False,
) -> Optional[UsersResponse]:
    """Get users

    Args:
        group_name (Union[Unset, str]):
        admin_data (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsersResponse
    """

    return sync_detailed(
        client=client,
        group_name=group_name,
        admin_data=admin_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: Union[Unset, str] = UNSET,
    admin_data: Union[Unset, bool] = False,
) -> Response[UsersResponse]:
    """Get users

    Args:
        group_name (Union[Unset, str]):
        admin_data (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsersResponse]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
        admin_data=admin_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    group_name: Union[Unset, str] = UNSET,
    admin_data: Union[Unset, bool] = False,
) -> Optional[UsersResponse]:
    """Get users

    Args:
        group_name (Union[Unset, str]):
        admin_data (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsersResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            group_name=group_name,
            admin_data=admin_data,
        )
    ).parsed
