from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.batch_chown_chmod import BatchChownChmod
from ...models.batch_chown_chmod_result import BatchChownChmodResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: BatchChownChmod,
    dry_run: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/_batch_chown_and_share".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["dryRun"] = dry_run

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[BatchChownChmodResult]:
    if response.status_code == HTTPStatus.OK:
        response_200 = BatchChownChmodResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[BatchChownChmodResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BatchChownChmod,
    dry_run: Union[Unset, None, bool] = False,
) -> Response[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, None, bool]):
        json_body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchChownChmodResult]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        dry_run=dry_run,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: BatchChownChmod,
    dry_run: Union[Unset, None, bool] = False,
) -> Optional[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, None, bool]):
        json_body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchChownChmodResult]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        dry_run=dry_run,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BatchChownChmod,
    dry_run: Union[Unset, None, bool] = False,
) -> Response[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, None, bool]):
        json_body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchChownChmodResult]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        dry_run=dry_run,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: BatchChownChmod,
    dry_run: Union[Unset, None, bool] = False,
) -> Optional[BatchChownChmodResult]:
    """Perform a batch of project ownership changes and projects shares

    Args:
        dry_run (Union[Unset, None, bool]):
        json_body (BatchChownChmod):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchChownChmodResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            dry_run=dry_run,
        )
    ).parsed
