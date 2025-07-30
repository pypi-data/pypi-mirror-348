from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document_hits import DocumentHits
from ...models.search_documents_search_type import SearchDocumentsSearchType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    query: Union[Unset, str] = "",
    from_: Union[Unset, int] = 0,
    size: Union[Unset, int] = 10,
    highlight: Union[Unset, bool] = False,
    facet: Union[Unset, bool] = False,
    query_filter: Union[Unset, str] = "",
    output_fields: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    search_type: Union[
        Unset, SearchDocumentsSearchType
    ] = SearchDocumentsSearchType.TEXT,
    native_rrf: Union[Unset, bool] = UNSET,
    vectorizer: Union[Unset, str] = UNSET,
    vector_query: Union[Unset, str] = "",
    html_version: Union[Unset, bool] = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params["from"] = from_

    params["size"] = size

    params["highlight"] = highlight

    params["facet"] = facet

    params["queryFilter"] = query_filter

    params["outputFields"] = output_fields

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, list[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["invertSearch"] = invert_search

    json_search_type: Union[Unset, str] = UNSET
    if not isinstance(search_type, Unset):
        json_search_type = search_type.value

    params["searchType"] = json_search_type

    params["nativeRRF"] = native_rrf

    params["vectorizer"] = vectorizer

    params["vectorQuery"] = vector_query

    params["htmlVersion"] = html_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_name}/documents/_search".format(
            project_name=project_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DocumentHits]:
    if response.status_code == 200:
        response_200 = DocumentHits.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DocumentHits]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    from_: Union[Unset, int] = 0,
    size: Union[Unset, int] = 10,
    highlight: Union[Unset, bool] = False,
    facet: Union[Unset, bool] = False,
    query_filter: Union[Unset, str] = "",
    output_fields: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    search_type: Union[
        Unset, SearchDocumentsSearchType
    ] = SearchDocumentsSearchType.TEXT,
    native_rrf: Union[Unset, bool] = UNSET,
    vectorizer: Union[Unset, str] = UNSET,
    vector_query: Union[Unset, str] = "",
    html_version: Union[Unset, bool] = False,
) -> Response[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        from_ (Union[Unset, int]):  Default: 0.
        size (Union[Unset, int]):  Default: 10.
        highlight (Union[Unset, bool]):  Default: False.
        facet (Union[Unset, bool]):  Default: False.
        query_filter (Union[Unset, str]):  Default: ''.
        output_fields (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        search_type (Union[Unset, SearchDocumentsSearchType]):  Default:
            SearchDocumentsSearchType.TEXT.
        native_rrf (Union[Unset, bool]):
        vectorizer (Union[Unset, str]):
        vector_query (Union[Unset, str]):  Default: ''.
        html_version (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        query=query,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        search_type=search_type,
        native_rrf=native_rrf,
        vectorizer=vectorizer,
        vector_query=vector_query,
        html_version=html_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    from_: Union[Unset, int] = 0,
    size: Union[Unset, int] = 10,
    highlight: Union[Unset, bool] = False,
    facet: Union[Unset, bool] = False,
    query_filter: Union[Unset, str] = "",
    output_fields: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    search_type: Union[
        Unset, SearchDocumentsSearchType
    ] = SearchDocumentsSearchType.TEXT,
    native_rrf: Union[Unset, bool] = UNSET,
    vectorizer: Union[Unset, str] = UNSET,
    vector_query: Union[Unset, str] = "",
    html_version: Union[Unset, bool] = False,
) -> Optional[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        from_ (Union[Unset, int]):  Default: 0.
        size (Union[Unset, int]):  Default: 10.
        highlight (Union[Unset, bool]):  Default: False.
        facet (Union[Unset, bool]):  Default: False.
        query_filter (Union[Unset, str]):  Default: ''.
        output_fields (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        search_type (Union[Unset, SearchDocumentsSearchType]):  Default:
            SearchDocumentsSearchType.TEXT.
        native_rrf (Union[Unset, bool]):
        vectorizer (Union[Unset, str]):
        vector_query (Union[Unset, str]):  Default: ''.
        html_version (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentHits
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        query=query,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        search_type=search_type,
        native_rrf=native_rrf,
        vectorizer=vectorizer,
        vector_query=vector_query,
        html_version=html_version,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    from_: Union[Unset, int] = 0,
    size: Union[Unset, int] = 10,
    highlight: Union[Unset, bool] = False,
    facet: Union[Unset, bool] = False,
    query_filter: Union[Unset, str] = "",
    output_fields: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    search_type: Union[
        Unset, SearchDocumentsSearchType
    ] = SearchDocumentsSearchType.TEXT,
    native_rrf: Union[Unset, bool] = UNSET,
    vectorizer: Union[Unset, str] = UNSET,
    vector_query: Union[Unset, str] = "",
    html_version: Union[Unset, bool] = False,
) -> Response[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        from_ (Union[Unset, int]):  Default: 0.
        size (Union[Unset, int]):  Default: 10.
        highlight (Union[Unset, bool]):  Default: False.
        facet (Union[Unset, bool]):  Default: False.
        query_filter (Union[Unset, str]):  Default: ''.
        output_fields (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        search_type (Union[Unset, SearchDocumentsSearchType]):  Default:
            SearchDocumentsSearchType.TEXT.
        native_rrf (Union[Unset, bool]):
        vectorizer (Union[Unset, str]):
        vector_query (Union[Unset, str]):  Default: ''.
        html_version (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentHits]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        query=query,
        from_=from_,
        size=size,
        highlight=highlight,
        facet=facet,
        query_filter=query_filter,
        output_fields=output_fields,
        simple_query=simple_query,
        selected_facets=selected_facets,
        invert_search=invert_search,
        search_type=search_type,
        native_rrf=native_rrf,
        vectorizer=vectorizer,
        vector_query=vector_query,
        html_version=html_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    from_: Union[Unset, int] = 0,
    size: Union[Unset, int] = 10,
    highlight: Union[Unset, bool] = False,
    facet: Union[Unset, bool] = False,
    query_filter: Union[Unset, str] = "",
    output_fields: Union[Unset, str] = "",
    simple_query: Union[Unset, bool] = False,
    selected_facets: Union[Unset, list[str]] = UNSET,
    invert_search: Union[Unset, bool] = False,
    search_type: Union[
        Unset, SearchDocumentsSearchType
    ] = SearchDocumentsSearchType.TEXT,
    native_rrf: Union[Unset, bool] = UNSET,
    vectorizer: Union[Unset, str] = UNSET,
    vector_query: Union[Unset, str] = "",
    html_version: Union[Unset, bool] = False,
) -> Optional[DocumentHits]:
    """Search for documents

    Args:
        project_name (str):
        query (Union[Unset, str]):  Default: ''.
        from_ (Union[Unset, int]):  Default: 0.
        size (Union[Unset, int]):  Default: 10.
        highlight (Union[Unset, bool]):  Default: False.
        facet (Union[Unset, bool]):  Default: False.
        query_filter (Union[Unset, str]):  Default: ''.
        output_fields (Union[Unset, str]):  Default: ''.
        simple_query (Union[Unset, bool]):  Default: False.
        selected_facets (Union[Unset, list[str]]):
        invert_search (Union[Unset, bool]):  Default: False.
        search_type (Union[Unset, SearchDocumentsSearchType]):  Default:
            SearchDocumentsSearchType.TEXT.
        native_rrf (Union[Unset, bool]):
        vectorizer (Union[Unset, str]):
        vector_query (Union[Unset, str]):  Default: ''.
        html_version (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentHits
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            query=query,
            from_=from_,
            size=size,
            highlight=highlight,
            facet=facet,
            query_filter=query_filter,
            output_fields=output_fields,
            simple_query=simple_query,
            selected_facets=selected_facets,
            invert_search=invert_search,
            search_type=search_type,
            native_rrf=native_rrf,
            vectorizer=vectorizer,
            vector_query=vector_query,
            html_version=html_version,
        )
    ).parsed
