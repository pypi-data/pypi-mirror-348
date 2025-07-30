from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.external_resources import ExternalResources
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    ignore_indexes: Union[Unset, None, str] = UNSET,
    ignore_databases: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/_external_resources".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ignoreIndexes"] = ignore_indexes

    params["ignoreDatabases"] = ignore_databases

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ExternalResources]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExternalResources.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ExternalResources]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ignore_indexes: Union[Unset, None, str] = UNSET,
    ignore_databases: Union[Unset, None, str] = UNSET,
) -> Response[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, None, str]):
        ignore_databases (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalResources]
    """

    kwargs = _get_kwargs(
        client=client,
        ignore_indexes=ignore_indexes,
        ignore_databases=ignore_databases,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    ignore_indexes: Union[Unset, None, str] = UNSET,
    ignore_databases: Union[Unset, None, str] = UNSET,
) -> Optional[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, None, str]):
        ignore_databases (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalResources]
    """

    return sync_detailed(
        client=client,
        ignore_indexes=ignore_indexes,
        ignore_databases=ignore_databases,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ignore_indexes: Union[Unset, None, str] = UNSET,
    ignore_databases: Union[Unset, None, str] = UNSET,
) -> Response[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, None, str]):
        ignore_databases (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalResources]
    """

    kwargs = _get_kwargs(
        client=client,
        ignore_indexes=ignore_indexes,
        ignore_databases=ignore_databases,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    ignore_indexes: Union[Unset, None, str] = UNSET,
    ignore_databases: Union[Unset, None, str] = UNSET,
) -> Optional[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, None, str]):
        ignore_databases (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalResources]
    """

    return (
        await asyncio_detailed(
            client=client,
            ignore_indexes=ignore_indexes,
            ignore_databases=ignore_databases,
        )
    ).parsed
