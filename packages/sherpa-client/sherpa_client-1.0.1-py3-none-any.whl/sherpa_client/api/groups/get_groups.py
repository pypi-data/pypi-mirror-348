from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_desc import GroupDesc
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    mapped: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["mapped"] = mapped

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/groups",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["GroupDesc"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_group_desc_array_item_data in _response_200:
            componentsschemas_group_desc_array_item = GroupDesc.from_dict(
                componentsschemas_group_desc_array_item_data
            )

            response_200.append(componentsschemas_group_desc_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["GroupDesc"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mapped: Union[Unset, bool] = False,
) -> Response[list["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GroupDesc']]
    """

    kwargs = _get_kwargs(
        mapped=mapped,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    mapped: Union[Unset, bool] = False,
) -> Optional[list["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GroupDesc']
    """

    return sync_detailed(
        client=client,
        mapped=mapped,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mapped: Union[Unset, bool] = False,
) -> Response[list["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GroupDesc']]
    """

    kwargs = _get_kwargs(
        mapped=mapped,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    mapped: Union[Unset, bool] = False,
) -> Optional[list["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GroupDesc']
    """

    return (
        await asyncio_detailed(
            client=client,
            mapped=mapped,
        )
    ).parsed
