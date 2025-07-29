from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_response import UserResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    username: str,
    *,
    admin_data: Union[Unset, bool] = True,
    jwt_format: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["adminData"] = admin_data

    params["jwtFormat"] = jwt_format

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users/{username}".format(
            username=username,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UserResponse]]:
    if response.status_code == 200:
        response_200 = UserResponse.from_dict(response.json())

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
) -> Response[Union[Any, UserResponse]]:
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
    admin_data: Union[Unset, bool] = True,
    jwt_format: Union[Unset, bool] = False,
) -> Response[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, bool]):  Default: True.
        jwt_format (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UserResponse]]
    """

    kwargs = _get_kwargs(
        username=username,
        admin_data=admin_data,
        jwt_format=jwt_format,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    admin_data: Union[Unset, bool] = True,
    jwt_format: Union[Unset, bool] = False,
) -> Optional[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, bool]):  Default: True.
        jwt_format (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UserResponse]
    """

    return sync_detailed(
        username=username,
        client=client,
        admin_data=admin_data,
        jwt_format=jwt_format,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    admin_data: Union[Unset, bool] = True,
    jwt_format: Union[Unset, bool] = False,
) -> Response[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, bool]):  Default: True.
        jwt_format (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UserResponse]]
    """

    kwargs = _get_kwargs(
        username=username,
        admin_data=admin_data,
        jwt_format=jwt_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    admin_data: Union[Unset, bool] = True,
    jwt_format: Union[Unset, bool] = False,
) -> Optional[Union[Any, UserResponse]]:
    """Get user

    Args:
        username (str):
        admin_data (Union[Unset, bool]):  Default: True.
        jwt_format (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UserResponse]
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
            admin_data=admin_data,
            jwt_format=jwt_format,
        )
    ).parsed
