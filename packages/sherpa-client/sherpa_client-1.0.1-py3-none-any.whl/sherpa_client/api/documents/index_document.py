from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ack import Ack
from ...models.index_document_indexes_item import IndexDocumentIndexesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    doc_id: str,
    *,
    indexes: Union[Unset, list[IndexDocumentIndexesItem]] = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_indexes: Union[Unset, list[str]] = UNSET
    if not isinstance(indexes, Unset):
        json_indexes = []
        for indexes_item_data in indexes:
            indexes_item = indexes_item_data.value
            json_indexes.append(indexes_item)

    params["indexes"] = json_indexes

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/documents/{doc_id}/_index".format(
            project_name=project_name,
            doc_id=doc_id,
        ),
        "params": params,
    }

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
    doc_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    indexes: Union[Unset, list[IndexDocumentIndexesItem]] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, list[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        doc_id=doc_id,
        indexes=indexes,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    doc_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    indexes: Union[Unset, list[IndexDocumentIndexesItem]] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, list[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
    """

    return sync_detailed(
        project_name=project_name,
        doc_id=doc_id,
        client=client,
        indexes=indexes,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    doc_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    indexes: Union[Unset, list[IndexDocumentIndexesItem]] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, list[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        doc_id=doc_id,
        indexes=indexes,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    doc_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    indexes: Union[Unset, list[IndexDocumentIndexesItem]] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, list[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Ack, Any]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            doc_id=doc_id,
            client=client,
            indexes=indexes,
        )
    ).parsed
