from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_chown_chmod import BatchChownChmod
from ...models.batch_chown_chmod_result import BatchChownChmodResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BatchChownChmod,
    dry_run: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["dryRun"] = dry_run

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/_batch_chown_and_share",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[BatchChownChmodResult]:
    if response.status_code == 200:
        response_200 = BatchChownChmodResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[BatchChownChmodResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BatchChownChmod,
    dry_run: Union[Unset, bool] = False,
) -> Response[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, bool]):  Default: False.
        body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchChownChmodResult]
    """

    kwargs = _get_kwargs(
        body=body,
        dry_run=dry_run,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BatchChownChmod,
    dry_run: Union[Unset, bool] = False,
) -> Optional[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, bool]):  Default: False.
        body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchChownChmodResult
    """

    return sync_detailed(
        client=client,
        body=body,
        dry_run=dry_run,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BatchChownChmod,
    dry_run: Union[Unset, bool] = False,
) -> Response[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, bool]):  Default: False.
        body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchChownChmodResult]
    """

    kwargs = _get_kwargs(
        body=body,
        dry_run=dry_run,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BatchChownChmod,
    dry_run: Union[Unset, bool] = False,
) -> Optional[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, bool]):  Default: False.
        body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchChownChmodResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            dry_run=dry_run,
        )
    ).parsed
