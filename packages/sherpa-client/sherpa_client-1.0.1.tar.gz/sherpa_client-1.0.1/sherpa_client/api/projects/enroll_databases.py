from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.external_databases import ExternalDatabases
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ExternalDatabases,
    deploy: Union[Unset, bool] = True,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["deploy"] = deploy

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/_enroll_databases",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ExternalDatabases]:
    if response.status_code == 200:
        response_200 = ExternalDatabases.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExternalDatabases]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExternalDatabases,
    deploy: Union[Unset, bool] = True,
) -> Response[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, bool]):  Default: True.
        body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalDatabases]
    """

    kwargs = _get_kwargs(
        body=body,
        deploy=deploy,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExternalDatabases,
    deploy: Union[Unset, bool] = True,
) -> Optional[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, bool]):  Default: True.
        body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalDatabases
    """

    return sync_detailed(
        client=client,
        body=body,
        deploy=deploy,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExternalDatabases,
    deploy: Union[Unset, bool] = True,
) -> Response[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, bool]):  Default: True.
        body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalDatabases]
    """

    kwargs = _get_kwargs(
        body=body,
        deploy=deploy,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExternalDatabases,
    deploy: Union[Unset, bool] = True,
) -> Optional[ExternalDatabases]:
    """enroll provided databases as project databases (response contains enrollment failures)

    Args:
        deploy (Union[Unset, bool]):  Default: True.
        body (ExternalDatabases):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalDatabases
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            deploy=deploy,
        )
    ).parsed
