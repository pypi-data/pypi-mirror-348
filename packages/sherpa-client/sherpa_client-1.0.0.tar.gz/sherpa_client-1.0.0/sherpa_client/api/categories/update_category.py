from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ack import Ack
from ...models.category_patch import CategoryPatch
from ...types import Response


def _get_kwargs(
    project_name: str,
    category_id: str,
    *,
    body: CategoryPatch,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/projects/{project_name}/categories/{category_id}".format(
            project_name=project_name,
            category_id=category_id,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/merge-patch+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Ack, Any]]:
    if response.status_code == 200:
        response_200 = Ack.from_dict(response.json())

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
) -> Response[Union[Ack, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    category_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CategoryPatch,
) -> Response[Union[Ack, Any]]:
    """Partially update a document category

    Args:
        project_name (str):
        category_id (str):
        body (CategoryPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        category_id=category_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    category_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CategoryPatch,
) -> Optional[Union[Ack, Any]]:
    """Partially update a document category

    Args:
        project_name (str):
        category_id (str):
        body (CategoryPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
    """

    return sync_detailed(
        project_name=project_name,
        category_id=category_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    category_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CategoryPatch,
) -> Response[Union[Ack, Any]]:
    """Partially update a document category

    Args:
        project_name (str):
        category_id (str):
        body (CategoryPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        category_id=category_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    category_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CategoryPatch,
) -> Optional[Union[Ack, Any]]:
    """Partially update a document category

    Args:
        project_name (str):
        category_id (str):
        body (CategoryPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            category_id=category_id,
            client=client,
            body=body,
        )
    ).parsed
