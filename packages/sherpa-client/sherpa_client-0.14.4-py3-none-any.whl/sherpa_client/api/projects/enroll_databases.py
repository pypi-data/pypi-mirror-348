from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.external_databases import ExternalDatabases
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: ExternalDatabases,
    deploy: Union[Unset, None, bool] = True,
) -> Dict[str, Any]:
    url = "{}/projects/_enroll_databases".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["deploy"] = deploy

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ExternalDatabases]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExternalDatabases.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ExternalDatabases]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ExternalDatabases,
    deploy: Union[Unset, None, bool] = True,
) -> Response[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, None, bool]):  Default: True.
        json_body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalDatabases]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        deploy=deploy,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: ExternalDatabases,
    deploy: Union[Unset, None, bool] = True,
) -> Optional[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, None, bool]):  Default: True.
        json_body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalDatabases]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        deploy=deploy,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ExternalDatabases,
    deploy: Union[Unset, None, bool] = True,
) -> Response[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, None, bool]):  Default: True.
        json_body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalDatabases]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        deploy=deploy,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: ExternalDatabases,
    deploy: Union[Unset, None, bool] = True,
) -> Optional[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, None, bool]):  Default: True.
        json_body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalDatabases]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            deploy=deploy,
        )
    ).parsed
