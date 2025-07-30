from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.ack import Ack
from ...models.index_document_indexes_item import IndexDocumentIndexesItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    indexes: Union[Unset, None, List[IndexDocumentIndexesItem]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents/{docId}/_index".format(
        client.base_url, projectName=project_name, docId=doc_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_indexes: Union[Unset, None, List[str]] = UNSET
    if not isinstance(indexes, Unset):
        if indexes is None:
            json_indexes = None
        else:
            json_indexes = []
            for indexes_item_data in indexes:
                indexes_item = indexes_item_data.value

                json_indexes.append(indexes_item)

    params["indexes"] = json_indexes

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Ack, Any]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Ack.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Ack, Any]]:
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
    client: Client,
    indexes: Union[Unset, None, List[IndexDocumentIndexesItem]] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, None, List[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        doc_id=doc_id,
        client=client,
        indexes=indexes,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    indexes: Union[Unset, None, List[IndexDocumentIndexesItem]] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, None, List[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
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
    client: Client,
    indexes: Union[Unset, None, List[IndexDocumentIndexesItem]] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, None, List[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        doc_id=doc_id,
        client=client,
        indexes=indexes,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    doc_id: str,
    *,
    client: Client,
    indexes: Union[Unset, None, List[IndexDocumentIndexesItem]] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Index a document already in db

    Args:
        project_name (str):
        doc_id (str):
        indexes (Union[Unset, None, List[IndexDocumentIndexesItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            doc_id=doc_id,
            client=client,
            indexes=indexes,
        )
    ).parsed
