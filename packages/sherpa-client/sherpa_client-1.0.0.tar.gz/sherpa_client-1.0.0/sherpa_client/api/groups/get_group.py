from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_desc import GroupDesc
from ...types import Response


def _get_kwargs(
    group_name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/groups/{group_name}".format(
            group_name=group_name,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GroupDesc]]:
    if response.status_code == 200:
        response_200 = GroupDesc.from_dict(response.json())

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
) -> Response[Union[Any, GroupDesc]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GroupDesc]]:
    """Get a users' group

    Args:
        group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupDesc]]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GroupDesc]]:
    """Get a users' group

    Args:
        group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GroupDesc]
    """

    return sync_detailed(
        group_name=group_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, GroupDesc]]:
    """Get a users' group

    Args:
        group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GroupDesc]]
    """

    kwargs = _get_kwargs(
        group_name=group_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, GroupDesc]]:
    """Get a users' group

    Args:
        group_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GroupDesc]
    """

    return (
        await asyncio_detailed(
            group_name=group_name,
            client=client,
        )
    ).parsed
