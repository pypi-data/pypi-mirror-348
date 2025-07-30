from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.group_desc import GroupDesc
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    mapped: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/groups".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["mapped"] = mapped

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["GroupDesc"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_group_desc_array_item_data in _response_200:
            componentsschemas_group_desc_array_item = GroupDesc.from_dict(componentsschemas_group_desc_array_item_data)

            response_200.append(componentsschemas_group_desc_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["GroupDesc"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    mapped: Union[Unset, None, bool] = False,
) -> Response[List["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GroupDesc']]
    """

    kwargs = _get_kwargs(
        client=client,
        mapped=mapped,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    mapped: Union[Unset, None, bool] = False,
) -> Optional[List["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GroupDesc']]
    """

    return sync_detailed(
        client=client,
        mapped=mapped,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    mapped: Union[Unset, None, bool] = False,
) -> Response[List["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GroupDesc']]
    """

    kwargs = _get_kwargs(
        client=client,
        mapped=mapped,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    mapped: Union[Unset, None, bool] = False,
) -> Optional[List["GroupDesc"]]:
    """Get users' groups

    Args:
        mapped (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GroupDesc']]
    """

    return (
        await asyncio_detailed(
            client=client,
            mapped=mapped,
        )
    ).parsed
