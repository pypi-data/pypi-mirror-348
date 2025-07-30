from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.search_terms_search_type import SearchTermsSearchType
from ...models.term_hits import TermHits
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, SearchTermsSearchType] = SearchTermsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/lexicons/_search".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["query"] = query

    params["from"] = from_

    params["size"] = size

    params["highlight"] = highlight

    params["facet"] = facet

    params["queryFilter"] = query_filter

    params["outputFields"] = output_fields

    params["simpleQuery"] = simple_query

    json_selected_facets: Union[Unset, None, List[str]] = UNSET
    if not isinstance(selected_facets, Unset):
        if selected_facets is None:
            json_selected_facets = None
        else:
            json_selected_facets = selected_facets

    params["selectedFacets"] = json_selected_facets

    params["invertSearch"] = invert_search

    json_search_type: Union[Unset, None, str] = UNSET
    if not isinstance(search_type, Unset):
        json_search_type = search_type.value if search_type else None

    params["searchType"] = json_search_type

    params["nativeRRF"] = native_rrf

    params["vectorizer"] = vectorizer

    params["vectorQuery"] = vector_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[TermHits]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TermHits.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[TermHits]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, SearchTermsSearchType] = SearchTermsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
) -> Response[TermHits]:
    """Search for terms

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, SearchTermsSearchType]):  Default:
            SearchTermsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TermHits]
    """

    kwargs = _get_kwargs(
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
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, SearchTermsSearchType] = SearchTermsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
) -> Optional[TermHits]:
    """Search for terms

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, SearchTermsSearchType]):  Default:
            SearchTermsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TermHits]
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
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, SearchTermsSearchType] = SearchTermsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
) -> Response[TermHits]:
    """Search for terms

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, SearchTermsSearchType]):  Default:
            SearchTermsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TermHits]
    """

    kwargs = _get_kwargs(
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
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    query: Union[Unset, None, str] = "",
    from_: Union[Unset, None, int] = 0,
    size: Union[Unset, None, int] = 10,
    highlight: Union[Unset, None, bool] = False,
    facet: Union[Unset, None, bool] = False,
    query_filter: Union[Unset, None, str] = "",
    output_fields: Union[Unset, None, str] = "",
    simple_query: Union[Unset, None, bool] = False,
    selected_facets: Union[Unset, None, List[str]] = UNSET,
    invert_search: Union[Unset, None, bool] = False,
    search_type: Union[Unset, None, SearchTermsSearchType] = SearchTermsSearchType.TEXT,
    native_rrf: Union[Unset, None, bool] = UNSET,
    vectorizer: Union[Unset, None, str] = UNSET,
    vector_query: Union[Unset, None, str] = "",
) -> Optional[TermHits]:
    """Search for terms

    Args:
        project_name (str):
        query (Union[Unset, None, str]):  Default: ''.
        from_ (Union[Unset, None, int]):
        size (Union[Unset, None, int]):  Default: 10.
        highlight (Union[Unset, None, bool]):
        facet (Union[Unset, None, bool]):
        query_filter (Union[Unset, None, str]):  Default: ''.
        output_fields (Union[Unset, None, str]):  Default: ''.
        simple_query (Union[Unset, None, bool]):
        selected_facets (Union[Unset, None, List[str]]):
        invert_search (Union[Unset, None, bool]):
        search_type (Union[Unset, None, SearchTermsSearchType]):  Default:
            SearchTermsSearchType.TEXT.
        native_rrf (Union[Unset, None, bool]):
        vectorizer (Union[Unset, None, str]):
        vector_query (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TermHits]
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
        )
    ).parsed
