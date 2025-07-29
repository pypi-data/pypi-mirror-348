from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.external_resources import ExternalResources
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    ignore_indexes: Union[Unset, str] = UNSET,
    ignore_databases: Union[Unset, str] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["ignoreIndexes"] = ignore_indexes

    params["ignoreDatabases"] = ignore_databases

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/_external_resources",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ExternalResources]:
    if response.status_code == 200:
        response_200 = ExternalResources.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExternalResources]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ignore_indexes: Union[Unset, str] = UNSET,
    ignore_databases: Union[Unset, str] = UNSET,
) -> Response[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, str]):
        ignore_databases (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalResources]
    """

    kwargs = _get_kwargs(
        ignore_indexes=ignore_indexes,
        ignore_databases=ignore_databases,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    ignore_indexes: Union[Unset, str] = UNSET,
    ignore_databases: Union[Unset, str] = UNSET,
) -> Optional[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, str]):
        ignore_databases (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalResources
    """

    return sync_detailed(
        client=client,
        ignore_indexes=ignore_indexes,
        ignore_databases=ignore_databases,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ignore_indexes: Union[Unset, str] = UNSET,
    ignore_databases: Union[Unset, str] = UNSET,
) -> Response[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, str]):
        ignore_databases (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalResources]
    """

    kwargs = _get_kwargs(
        ignore_indexes=ignore_indexes,
        ignore_databases=ignore_databases,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    ignore_indexes: Union[Unset, str] = UNSET,
    ignore_databases: Union[Unset, str] = UNSET,
) -> Optional[ExternalResources]:
    """List non-sherpa indexes and databases

    Args:
        ignore_indexes (Union[Unset, str]):
        ignore_databases (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalResources
    """

    return (
        await asyncio_detailed(
            client=client,
            ignore_indexes=ignore_indexes,
            ignore_databases=ignore_databases,
        )
    ).parsed
